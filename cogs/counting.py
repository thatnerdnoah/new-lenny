from discord import TextChannel, Embed, Colour, app_commands, Interaction
from discord.ext import commands
from helpers import database
from media import meme
import asyncio

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
        
    async def cog_load(self) -> None:
        self.initialize_cog()

    async def cog_unload(self) -> None:
        self.bot.remove_listener(self.on_message)

    @commands.Cog.listener()
    async def on_ready(self):
        self.initialize_cog()

    def initialize_cog(self):
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

    # Commands for setting the count, restoring count, and setting the number of lives
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

    @app_commands.command(name="setlives", description="Set the number of lives")
    @app_commands.describe(lives_to_set="Number of lives to set the bot to")
    @app_commands.rename(lives_to_set="lives")
    async def set_lives(self, interaction: Interaction, lives_to_set: int):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("How did you find this command?", ephemeral=True)
        
        # Sets the lives, with a max amount of lives to 3
        try:
            return_number = lives_to_set
            # We do not want more than 3 lives as this can make the count go longer than it should
            if return_number > 3:
                return_number = 3
                print(f"Lives was inputted as {lives_to_set}. Setting to {return_number}.")

            self.lives = return_number
            database.update_lives(self.lives)
            await interaction.response.send_message(f"Lives have been set to {return_number}!", ephemeral=True)
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
                                await asyncio.sleep(0.1)
                                await message.add_reaction("❌")
                                await message.channel.send(f"You cannot go twice in a row, <@{message.author.id}>!")
                                await message.channel.send(f"Counting may continue at {self.expected_number}!")
                                return

                    if message_number == self.expected_number: 
                        self.last_messanger = message.author
                        await meme.handle_number(message=message, number=self.expected_number)
                        
                        if self.expected_number == self.record + 1:
                            await message.channel.send("You broke the record!")
                        
                        self.expected_number += 1
                        database.database_push(self.expected_number)
                        await asyncio.sleep(0.1)
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
                            await asyncio.sleep(0.1)
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

                            await asyncio.sleep(0.1)
                            await message.add_reaction("❌")
                            await message.channel.send(f"<@{message.author.id}> cant count!")
                            if self.lives == 1:
                                await message.channel.send(f"There is one life left! Don't waste it!")
                            else:
                                await message.channel.send(f"There are {self.lives} lives left!")
                except Exception:
                    return   
        else: 
            return
            
async def setup(bot):
    await bot.add_cog(Counting(bot))   