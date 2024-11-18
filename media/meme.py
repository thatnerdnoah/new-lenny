import random as rand
from discord import File

async def upload_meme(message, number):
    if number == 1:
        await message.channel.send(file=File("./media/1.jpg"))
    elif number == 10:
        ben_tits = rand.randint(0,1)
        if ben_tits == 0:
            await message.channel.send("woah 10 bits!")
        elif ben_tits == 1:
            await message.channel.send("woah ben tits!")
        else:
            await message.channel.send("woah 10 bits!")
    elif number == 21:
        await message.channel.send(file=File("./media/21.gif"))
    elif number == 25:
        await message.channel.send(file=File("./media/25.gif"))
    elif number == 42:
        await message.channel.send("the meaning of life")
    elif number == 51:
        aliens = rand.randint(0,1)
        if aliens == 0:
            await message.channel.send(file=File("./media/51.gif"))
        elif aliens == 1:
            await message.channel.send(file=File("./media/51.jpg"))
        else:
            await message.channel.send("woah 10 bits!")
    elif number == 66:
        await message.channel.send(file=File("./media/66.gif"))
    elif number == 69:
        await message.channel.send("nice", file=File("./media/69.png"))
    # elif self.expected_number == 96:
    #     await message.channel.send("not nice")
    elif number == 100:
        await message.channel.send(file=File("./media/100.gif"))
    elif number == 111:
        await message.channel.send(file=File("./media/111.gif"))
    # elif self.expected_number == 137:
    #     await message.channel.send("MAX LAFF POI... wait")
    elif number == 140:
        await message.channel.send("MAX LAFF POINTS!")
    elif number == 222:
        await message.channel.send(file=File("./media/222.gif"))
    elif number == 305:
        await message.channel.send("Dale???? Idk who dale is")
    elif number == 314:
        await message.channel.send(file=File("./media/314.gif"))
    elif number == 321:
        await message.channel.send(file=File("./media/321.gif"))
    elif number == 333:
        await message.channel.send(file=File("./media/333.gif"))
    elif number == 404:
        await message.channel.send("Error: not found", file=File("./media/404.gif"))
    elif number == 420:
        await message.channel.send("BLAZE IT!", file=File("./media/420.gif"))
    elif number == 444:
        await message.channel.send(file=File("./media/444.gif"))