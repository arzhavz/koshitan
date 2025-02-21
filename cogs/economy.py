import asyncio
import discord
import random
import json 

from discord.ext import commands
from discord.ext.commands import Context

from lib import Interface
from lib.games.slot import Slot


class Economy(commands.Cog, name="economy"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="claim", description="Claim random amount of moneys every 15 minutes."
    )
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def claim(self, context: Context) -> None:
        """
        Claim random amount of moneys
        """
        user = await self.bot.database.connect_user(context.author.id)
        moneys = round(random.random() * (950 + (1000 * 0.05 * user["level"]))) 
        user["money"] += moneys
        embed = discord.Embed(
            description=f"Success claim {moneys:,} <:rupiah:1334623817850552341>\nNext claim in 15 minutes.",
            color=0xBEBEFE,
        )
        embed.set_footer(text=f"Requested by {context.author}.")
        await context.send(embed=embed)
        await self.bot.database.update_user(context.author.id, user)

    @commands.hybrid_command(
        name="coinflip",
        description="Make a coin flip, but give your bet before.",
        aliases=["cf"],
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coinflip(self, context: Context, bet: str = None) -> None:
        """
        Make a coin flip, but give your bet before.
        """
        if bet is None:
            embed = discord.Embed(description="Please input your bet.", color=0xE02B2B)
            embed.set_footer(text=f"Requested by {context.author}.")
            message = await context.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return
        user = await self.bot.database.connect_user(context.author.id)
        button = Interface.Button(context.author)
        buttons = button.create([("Tails", "tails"), ("Heads", "heads")])
        if bet == "all":
            bet = user["money"]
        bet = int(bet)
        if bet > user["money"] or user["money"] == 0:
            embed = discord.Embed(
                description=f"Insufficient money to make a bet, your balance is: {user['money']:,} <:rupiah:1334623817850552341>",
                color=0xE02B2B,
            )
            embed.set_footer(text=f"Requested by {context.author}.")
            message = await context.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return
        embed = discord.Embed(description="What is your choice?", color=0xBEBEFE)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()
        result = random.choice(["heads", "tails"])
        user["money"] -= bet
        if buttons.value == result:
            user["money"] += bet * 2
            await self.bot.database.update_user(context.author.id, user)
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.\nYou got: {bet:,} <:rupiah:1334623817850552341>",
                color=0xBEBEFE,
            )
            embed.set_footer(text=f"Requested by {context.author}.")
        else:
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`. \nYou lost: {bet:,} <:rupiah:1334623817850552341>",
                color=0xE02B2B,
            )
            embed.set_footer(text=f"Requested by {context.author}.")
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(name="slot", description="Wanna play slots?")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slot(self, context: Context, bet: str = None) -> None:
        """
        Sebuah permainan slot
        """
        if bet is None:
            embed = discord.Embed(
                description="Please input your bet, or add `help` for game's rules.",
                color=0xE02B2B,
            )
            embed.set_footer(text=f"Requested by {context.author}.")
            message = await context.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return
        if bet == "help":
            embed = discord.Embed(
                description=(
                    "**Slot Machine Game Mechanics & Payout Calculation**\n\n"
                    "**Game Overview:**\n"
                    "The slot machine game features a **6x4 grid** filled with random symbols. Players place a bet, "
                    "and the game generates symbols on the grid. Winning patterns determine the payout.\n\n"
                    "**Symbol Categories & Probability Distribution:**\n"
                    "- **Fruits (🍒, 🍓, 🫐, 🥭, 🍍, 🍋, 🍌, 🍉, 🍇, 🥝)** – 70% chance\n"
                    "- **Card Suits (♠️, ♣️, ♥️, ♦️)** – 20% chance\n"
                    "- **High-Value Objects (💵, 💰, 🏆)** – 9.9% chance\n"
                    "- **Lucky Seven (7️⃣)** – 0.1% chance\n\n"
                    "**Winning Patterns & Multiplier Calculation:**\n"
                    "- Each symbol has a **base multiplier**:\n"
                    "  - Fruits: **0.0075x**\n"
                    "  - Card Suits: **0.0175x**\n"
                    "  - High-Value Objects: **0.275x**\n"
                    "  - Lucky Seven (7️⃣): **5.625x**\n"
                    "- Bonus multiplier based on wildcards (`x`):\n"
                    "  - **3 Fixed Matches** → `1x`\n"
                    "  - **2 Fixed Matches + 1 Wildcard** → `1.25x`\n"
                    "  - **1 Fixed Match + 2 Wildcards** → `2.5x`\n"
                    "  - **All Wildcards** → `5x`\n\n"
                    "**Example Calculation:**\n"
                    "- **Bet: 100 <:rupiah:1334623817850552341>**\n"
                    "- **Winning pattern:** 2 💵 symbols + 1 wildcard (`x`)\n"
                    "- Base multiplier: **0.275 + 0.275 = 0.55x**\n"
                    "- Wildcard bonus: **1.25x**\n"
                    "- Total multiplier: **0.55 × 1.25 = 0.6875x**\n"
                    "- **Payout: 100 × 0.6875 = 69 <:rupiah:1334623817850552341>**\n\n"
                    "**Game Flow:**\n"
                    "1️⃣ Place a bet.\n"
                    "2️⃣ The slot generates a **6x4 grid** of random symbols.\n"
                    "3️⃣ The system evaluates multiple winning patterns.\n"
                    "4️⃣ If a pattern is triggered, the payout is calculated.\n"
                    "5️⃣ Total winnings are awarded based on all triggered patterns.\n\n"
                ),
                color=0xBEBEFE,
            )
            embed.set_author(name="🎰 Slots Help")
            embed.set_footer(text=f"Requested by {context.author}.")
            await context.send(embed=embed)
            return

        user = await self.bot.database.connect_user(context.author.id)
        if bet == "all":
            bet = user["money"]
        bet = int(bet)
        if bet > user["money"] or user["money"] == 0:
            embed = discord.Embed(
                description=f"Insufficient money to make a bet, your balance is: {user['money']:,} <:rupiah:1334623817850552341>",
                color=0xE02B2B,
            )
            embed.set_footer(text=f"Requested by {context.author}.")
            message = await context.send(embed=embed)
            await asyncio.sleep(5)
            await message.delete()
            return
        user["money"] -= bet
        patterns = random.randint(10000, 100000)
        slot = Slot(bet, patterns).play_game()
        user["money"] += slot["rewards"]
        reward = f"{slot['rewards']:,} <:rupiah:1334623817850552341>" if slot["rewards"] > 0 else "You got nothing!"
        embed = discord.Embed(
            description=f"\n{slot['emotes']}\n\nBet: {bet:,} <:rupiah:1334623817850552341>\nReward: {reward}",
            color=0xBEBEFE,
        )
        embed.set_author(name="🎰 Slots")
        embed.set_footer(text=f"Requested by {context.author}.")
        await self.bot.database.update_user(context.author.id, user)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="balance", description="Display user balance.", aliases=["bal"]
    )
    async def balance(self, context: Context) -> None:
        user = await self.bot.database.connect_user(context.author.id)
        embed = discord.Embed(
            description=f"Your balance is: {user['money']:,} <:rupiah:1334623817850552341>", color=0xBEBEFE
        )
        embed.set_footer(text=f"Requested by {context.author}.")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="profile",
        description="Display your information.",
        aliases=["profil"]
    )
    async def profile(self, context: Context) -> None:
        user = await self.bot.database.connect_user(context.author.id)
        crate = json.loads(user["crate"])
        embed = discord.Embed(
            description=(
                "**<:pprofile:1334628047273332757> Profile**\n"
                f"- Name: <@{context.author.id}>\n"
                f"- Money: {user['money']:,} <:rupiah:1334623817850552341>\n"
                f"- Level: {user['level']}\n"
                f"- Exp: {user['exp']} | {Interface.Misc.progress_bar(user['exp'], 750, 32)}"
            ), color=0xBEBEFE
        )
        embed.set_author(name="User Information")
        embed.set_footer(text=f"Requested by {context.author}.")
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Economy(bot))
