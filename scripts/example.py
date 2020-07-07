import os
import random
import discord
import pandas as pd
import numpy as np

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def binomial(k, n, p, s=10000):

    return np.sum(np.random.binomial(n, p, s) == k) / s


def at_least(prob, k, n, p):

    return sum([prob(i, n, p) for i in range(k, n + 1)])


def get_table(prob, tries: int, die: int):

    sucesseses = range(1, tries + 1)
    difficulties = range(1, die + 1)

    df = pd.DataFrame(
        [
            [
                at_least(binomial, sucesses, tries, 1 - ((difficulty - 1) / 10))
                for difficulty in difficulties
            ]
            for sucesses in sucesseses
        ],
        columns=difficulties,
        index=sucesseses,
    )

    return "```\n" + df.to_markdown(tablefmt="simple", floatfmt=".1f") + "\n```"


def to_table(args):

    args = args.split(" ")

    tries, die = args[0].split("d")

    return get_table(binomial, int(tries), int(die))


bot = commands.Bot(command_prefix="!")


@bot.command(name="f", help="Simulates rolling dice.")
async def roll(ctx, *, roll: to_table):

    await ctx.send("Sucess\Difficulty\n" + roll)


bot.run(TOKEN)
