import random as rand
from discord import File

# Mapping numbers to responses
response_map = {
    1: lambda: {"file": File("./media/1.jpg")},
    21: lambda: {"file": File("./media/21.gif")},
    25: lambda: {"file": File("./media/25.gif")},
    42: lambda: {"content": "the meaning of life"},
    66: lambda: {"file": File("./media/66.gif")},
    69: lambda: {"content": "nice", "file": File("./media/69.png")},
    100: lambda: {"file": File("./media/100.gif")},
    111: lambda: {"file": File("./media/111.gif")},
    140: lambda: {"content": "MAX LAFF POINTS!"},
    222: lambda: {"file": File("./media/222.gif")},
    305: lambda: {"content": "Dale???? Idk who dale is"},
    314: lambda: {"file": File("./media/314.gif")},
    321: lambda: {"file": File("./media/321.gif")},
    333: lambda: {"file": File("./media/333.gif")},
    404: lambda: {"content": "Error: not found", "file": File("./media/404.gif")},
    420: lambda: {"content": "BLAZE IT!", "file": File("./media/420.gif")},
    444: lambda: {"file": File("./media/444.gif")},
    777: lambda: {"file": File("./media/777.gif")},
}

# Special cases
def special_10():
    ben_tits = rand.randint(0, 1)
    return {"content": "woah 10 bits!"} if ben_tits == 0 else {"content": "woah ben tits!"}

def special_51():
    aliens = rand.randint(0, 1)
    return {"file": File("./media/51.gif")} if aliens == 0 else {"file": File("./media/51.jpg")}

special_cases = {
    10: special_10,
    51: special_51,
}

# Main handler function
async def handle_number(number, message):
    if number in special_cases:
        response = special_cases[number]()
    elif number in response_map:
        response = response_map[number]()
    else:
        return  # No action for unhandled numbers

    # Send the message
    if "content" in response and "file" in response:
        await message.channel.send(response["content"], file=response["file"])
    elif "content" in response:
        await message.channel.send(response["content"])
    elif "file" in response:
        await message.channel.send(file=response["file"])
