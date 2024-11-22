from discord import TextChannel, File, Embed, Colour, app_commands, Interaction
from discord.ext import commands
from helpers import database
from media import meme
import random as rand

local_test = False

try:
    import config_local as config
    local_test = True
except ImportError:
    import config


class Counting(commands.Cog, name="Counting"):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.counting_channel : TextChannel = None
        self.log_channel : TextChannel = None
        self.collect : bool = False
        self.last_messanger = None
        self.expected_number = 1
        self.record = 0
        self.lives = 3
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.counting_channel = self.bot.get_channel(config.counting_channel)
        self.log_channel = self.bot.get_channel(config.log_channel)

        print("Before database pull:", self.expected_number, self.record, self.lives)
        
        db_number, record_number, lives = database.database_pull()

        if db_number != 0:
            self.expected_number = db_number
            self.record = record_number
            self.lives = lives

        print("After database pull:", self.expected_number, self.record, self.lives)
        print("Counting begins!")

    # old command with the prefix
    @app_commands.command(name="countnumber", description="Set the next number for counting")
    @app_commands.describe(number_to_set="The number to set the count to")
    @app_commands.rename(number_to_set="number")
    async def set_number(self, interaction: Interaction, number_to_set: int):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("How did you find this command?", ephemeral=True)
        
        print("Command sent to set current number to", number_to_set)
        self.expected_number = number_to_set
        database.database_push(self.expected_number)
        await interaction.response.send_message(f"Counting's next number has been set to {self.expected_number}!", ephemeral=True)

    @app_commands.command(name="restorecount", description="Restore the count to the previous highest number")
    async def restore_number(self, interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("How did you find this command?", ephemeral=True)
        
        try:
            print("Count will be restored")
            # current count variable for embed
            current_count = self.expected_number
            backup_number = database.pull_backup()
            if backup_number == 0:
                raise ValueError("The number must be greater than 0.")
            
            self.expected_number = backup_number
            embed = Embed(
                title="The counting has been restored!",
                type='rich',
                colour=Colour.purple()
            )
            embed.add_field(name="Current count before restore", value=current_count, inline=False)
            embed.add_field(name="Next number to type in", value=backup_number, inline=False)
            await self.log_channel.send(embed=embed)
            await interaction.response.send_message("Count has been restored! Check #logs for more info!", ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message("The value of the backup number was 0! Set the count manually.", ephemeral=True)
            print(f"Error: {e}")
        except Exception as e:
            await interaction.response.send_message("Something went wrong!", ephemeral=True)
            print(f"Error: {e}")
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel == self.counting_channel:
            if message.author != self.bot.user:
                try:
                    message_number = int(message.content)
                    if not local_test:
                        if message.author == self.last_messanger:
                                await message.add_reaction("❌")
                                await message.channel.send(f"You cannot go twice in a row, <@{message.author.id}>!")
                                await message.channel.send(f"Counting may continue at {self.expected_number}!")
                                return

                    if message_number == self.expected_number: 
                        self.last_messanger = message.author
                        await meme.upload_meme(message=message, number=self.expected_number)
                        
                        if self.expected_number == self.record + 1:
                            await message.channel.send("You broke the record!")
                        
                        self.expected_number += 1
                        database.database_push(self.expected_number)
                        await message.add_reaction("✅")
                    else:
                        if self.lives <= 1:
                            # Embed log
                            embed = Embed(
                                title="The counting stopped!",
                                type='rich',
                                colour=Colour.purple()
                            )
                            embed.add_field(name="Expected number", value=self.expected_number, inline=False)
                            embed.add_field(name="Number typed in", value=message_number, inline=False)
                            await self.log_channel.send(embed=embed)
                            
                            # set the record
                            if self.expected_number > self.record:
                                self.record = self.expected_number
                                database.update_record(self.record)

                            # reset the counter
                            database.database_copy(self.expected_number)
                            self.expected_number = 1
                            database.database_push(self.expected_number)
                            self.last_messanger = None
                            self.lives = 3
                            database.update_lives(self.lives)
                            await message.add_reaction("❌")
                            await message.channel.send(f"<@{message.author.id}> cant count!")
                        else:
                            self.lives -= 1
                            database.update_lives(self.lives)
                            
                            embed = Embed(
                                title="A life was used on counting!",
                                type='rich',
                                colour=Colour.purple()
                            )
                            embed.add_field(name="Expected number", value=self.expected_number, inline=False)
                            embed.add_field(name="Number typed in", value=message_number, inline=False)
                            embed.add_field(name="Number of lives left", value=self.lives, inline=False)
                            await self.log_channel.send(embed=embed)

                            await message.add_reaction("❌")
                            await message.channel.send(f"<@{message.author.id}> cant count!")
                            if self.lives == 1:
                                await message.channel.send(f"You have one life left! Don't waste it!")
                            else:
                                await message.channel.send(f"You have {self.lives} lives left!")

                except Exception:
                    return   
        else: 
            return
            
async def setup(client):
    await client.add_cog(Counting(client))
    