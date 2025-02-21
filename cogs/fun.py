import random

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import Context

from lib import Interface


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                embed.set_footer(text=f"Requested by {context.author}.")
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """

        select = Interface.Select(context)
        action = select(
            message="Please select your choice",
            value=[
                ("Scissors", "scissors", "You choose scissors.", "✂"),
                ("Rock", "rock", "You choose rock.", "🪨"),
                ("Paper", "paper", "You choose paper.", "🧻"),
            ],
        )
        response = await action.show()
        if not response:
            return

        user_choice = response.response
        bot_choice = random.choice(["scissors", "rock", "paper"])

        if user_choice == bot_choice:
            result = "It's a tie!"
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "scissors" and bot_choice == "paper") or \
             (user_choice == "paper" and bot_choice == "rock"):
            result = "You win! 🎉"
        else:
            result = "You lose! 😢"

        await context.send(f"You chose {user_choice} {dict(scissors='✂', rock='🪨', paper='🧻')[user_choice]}\n"
                           f"The bot chose {bot_choice} {dict(scissors='✂', rock='🪨', paper='🧻')[bot_choice]}\n"
                           f"**{result}**")



async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))
