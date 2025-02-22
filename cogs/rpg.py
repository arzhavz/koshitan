import discord
import json
import time
import random

from typing import Optional, List

from rich.pretty import pprint

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from lib import Interface

from lib.games.rpg import RPGame, Utils
from lib.games.rpg_chars import Hero
from lib.games.rpg_message import Messages

class RPG(commands.Cog, name="rpg"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="inventory",
        description="Display your inventory.",
        aliases=["inv"]
    )
    async def inventory(self, context: Context) -> None:
        user = await self.bot.database.connect_user(context.author.id)
        crate = json.loads(user["crate"])
        item = json.loads(user["item"])
        energy = json.loads(user["energy"])
        embed = discord.Embed(
            description=(
                "**<:pprofile:1334628047273332757> Profile**\n"
                f"- Name: <@{context.author.id}>\n"
                f"- Money: {user['money']:,} <:rupiah:1334623817850552341>\n"
                f"- Level: {user['level']}\n"
                f"- Exp: {user['exp']} | {Interface.Misc.progress_bar(user['exp'], 750, 32)}\n"
                f"- Energy:  {Interface.Misc.progress_bar(energy['energy'], energy['max'], 32)}\n\n"
                "**<:woodencrate:1334631694870773780> Crates**\n"
                f"- <:commoncrate:1335016425827471491> Common: {crate['common']} \n"
                f"- <:uncommoncrate:1335016439085666408> Uncommon: {crate['uncommon']} \n"
                f"- <:rarecrate:1335016450381054155> Rare: {crate['rare']} \n"
                f"- <:epiccrate:1335016472044634242> Epic: {crate['epic']} \n"
                f"- <:legendarycrate:1335016485134798888> Legendary: {crate['legendary']} \n"
                f"- <:treasurechest:1336017158668554290> Treasure: {crate['treasure']}\n\n"
                "**<:crate:1334632914998132870> Items**\n"
                f"- Wheat: {item['wheat']:,} <:wheat1:1334677575368441926>\n"
                f"- Wood: {item['wood']:,} <:wood1:1334677714141188137>\n"
                f"- Stone: {item['stone']:,} <:stone1:1334677658944143422>\n"
                f"- Steel: {item['steel']:,} <:steel1:1334677767941525544>\n"
                f"- Trash: {item['trash']:,} <:trash1:1334677517277069452>\n"

            ), color=0xBEBEFE
        )
        embed.set_author(name="User Inventory")
        embed.set_footer(text=f"Requested by {context.author}.")
        await context.send(embed=embed) 

    @commands.hybrid_command(
        name="crate",
        description="Manage your crates."
    )
    async def crate(self, context: Context, menu: str = None) -> None:
        user = await self.bot.database.connect_user(context.author.id)
        crate = json.loads(user["crate"])
        energy = json.loads(user["energy"])
        if menu == "add":
            select = Interface.Select(context)
            action = select("Select your crate.", [
                ("Treasure", "treasure", "Add 1,000,000 crate(s).", "<:treasurechest:1336017158668554290>"),
                ("Common", "common", "Add 10 crate(s).", "<:commoncrate:1335016425827471491>"),
                ("Uncommon", "uncommon", "Add 10 crate(s).", "<:uncommoncrate:1335016439085666408>"),
                ("Rare", "rare", "Add 10 crate(s).", "<:rarecrate:1335016450381054155>"),
                ("Epic", "epic", "Add 10 crate(s).", "<:epiccrate:1335016472044634242>"),
                ("Legendary", "legendary", "Add 10 crate(s).", "<:legendarycrate:1335016485134798888>")
            ])
            response = await action.show()
            crate[response.response] += 1000000 if response.response == "treasure" else 10
            user["crate"] = json.dumps(crate)
            await self.bot.database.update_user(context.author.id, user)
            await context.send(f"Increased {response.response.capitalize()} crate.")
            return

        if menu == "open":
            rewards = {
                "wheat": 0,
                "wood": 0,
                "stone": 0,
                "steel": 0,
                "trash": 0
            }
            item = {
                "wheat": "<:wheat1:1334677575368441926>",
                "wood": "<:wood1:1334677714141188137>",
                "stone": "<:stone1:1334677658944143422>",
                "steel": "<:steel1:1334677767941525544>",
                "trash": "<:trash1:1334677517277069452>"
            }
            moneys = 0
            select = Interface.Select(context)
            action = select("Select your crate.", [
                ("Treasure", "treasure", f"You have: {crate['treasure']} treasure crate(s), select to open all.", "<:treasurechest:1336017158668554290>"),
                ("Common", "common", f"You have: {crate['common']} common crate(s), select to open all.", "<:commoncrate:1335016425827471491>"),
                ("Uncommon", "uncommon", f"You have: {crate['uncommon']} uncommon crate(s), select to open all.", "<:uncommoncrate:1335016439085666408>"),
                ("Rare", "rare", f"You have: {crate['rare']} rare crate(s), select to open all.", "<:rarecrate:1335016450381054155>"),
                ("Epic", "epic", f"You have: {crate['epic']} epic crate(s), select to open all.", "<:epiccrate:1335016472044634242>"),
                ("Legendary", "legendary", f"You have: {crate['legendary']} legendary crate(s), select to open all.", "<:legendarycrate:1335016485134798888>")
            ])
            response = await action.show()

            if crate[response.response] <= 0:
                return await context.send("You have 0 crate(s)!")
            
            if response.response == "treasure":
                for _ in range(crate[response.response]):
                    money, crates = RPGame(user).open_crate(response.response)
                    user["crate"] = json.dumps(crates)
                    moneys += money
                embed = discord.Embed(
                    description=(
                        "**Open Crate**\n\n"
                        "You got:\n"
                        f"- Money: {moneys:,} <:rupiah:1334623817850552341>\n"
                    ),
                    color=0xBEBEFE
                )
            else:
                for _ in range(crate[response.response]):
                    res, money, (crates, items) = RPGame(user).open_crate(response.response)
                    user["crate"] = json.dumps(crates)
                    user["item"] = json.dumps(items)
                    for i, qty in res.items():
                        rewards[i] += qty
                    moneys += money

                embed = discord.Embed(
                    description=(
                        "**Open Crate**\n\n"
                        "You got:\n"
                        f"- Money: {moneys:,} <:rupiah:1334623817850552341>\n"
                        + "\n".join(f"- {label.capitalize()}: {qty:,} {item[label]}" for label, qty in rewards.items())  
                        + f"\n- Total: {sum(rewards.values()):,} items." 
                    ),
                    color=0xBEBEFE
                )
            
            await self.bot.database.update_user(context.author.id, user)
            embed.set_footer(text=f"Requested by {context.author}.")
            return await context.send(embed=embed)
        
        embed = discord.Embed(
            description=(
                "**<:pprofile:1334628047273332757> Profile**\n"
                f"- Name: <@{context.author.id}>\n"
                f"- Money: {user['money']:,} <:rupiah:1334623817850552341>\n"
                f"- Level: {user['level']}\n"
                f"- Exp: {user['exp']} | {Interface.Misc.progress_bar(user['exp'], 750, 32)}\n"
                f"- Energy: {Interface.Misc.progress_bar(energy['energy'], energy['max'], 32)}\n\n"
                "**<:woodencrate:1334631694870773780> Crates**\n"
                f"- <:commoncrate:1335016425827471491> Common: {crate['common']} \n"
                f"- <:uncommoncrate:1335016439085666408> Uncommon: {crate['uncommon']} \n"
                f"- <:rarecrate:1335016450381054155> Rare: {crate['rare']} \n"
                f"- <:epiccrate:1335016472044634242> Epic: {crate['epic']} \n"
                f"- <:legendarycrate:1335016485134798888> Legendary: {crate['legendary']} \n"
                f"- <:treasurechest:1336017158668554290> Treasure: {crate['treasure']}\n\n"
                "**Helps**\n"
                "- To open your crate(s), add command `open` and select crate(s) rarities.\n\n"
                "<:treasurechest:1336017158668554290> **Treasure Crate:**\n"
                " - Guaranteed to contain up to **250,000** <:rupiah:1334623817850552341>.\n"
                "<:commoncrate:1335016425827471491> **Common Crate:**\n"
                " - Guaranteed to contain up to **1,000** <:rupiah:1334623817850552341>.\n"
                " - Includes up to **3 random item types**, with a total of up to **50 items**.\n"
                "<:uncommoncrate:1335016439085666408> **Uncommon Crate:**\n"
                " - Guaranteed to contain up to **2,500** <:rupiah:1334623817850552341>.\n"
                " - Includes up to **4 random item types**, with a total of up to **200 items**.\n"
                "<:rarecrate:1335016450381054155> **Rare Crate:**\n"
                " - Guaranteed to contain up to **7,500** <:rupiah:1334623817850552341>.\n"
                " - Includes up to **5 random item types**, with a total of up to **500 items**.\n"
                "<:epiccrate:1335016472044634242> **Epic Crate:**\n"
                " - Guaranteed to contain up to **20,000** <:rupiah:1334623817850552341>.\n"
                " - Contains **all item types randomly**, with a total of up to **1,000 items**.\n"
                "<:legendarycrate:1335016485134798888> **Legendary Crate:**\n"
                " - Guaranteed to contain up to **150,000** <:rupiah:1334623817850552341>.\n"
                " - Contains **all item types randomly**, with a total of up to **2,500 items**."
            ), color=0xBEBEFE
        )
        embed.set_author(name="User Crates")
        embed.set_footer(text=f"Requested by {context.author}.")
        await context.send(embed=embed) 

    @commands.hybrid_command(
        name="stroll",
        description="Strolling around the world, receive some sources."
    )
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def stroll(self, context: Context) -> None:
        item_e = {
                "wheat": "<:wheat1:1334677575368441926>",
                "wood": "<:wood1:1334677714141188137>",
                "stone": "<:stone1:1334677658944143422>",
                "steel": "<:steel1:1334677767941525544>",
                "trash": "<:trash1:1334677517277069452>"
            }
        crates = [
            ("treasure", 0.3),
            ("common", 0.3),
            ("uncommon", 0.2),
            ("rare", 0.1),
            ("epic", 0.095),
            ("legendary", 0.005)
        ]
        crate_e = {
            "treasure": "<:treasurechest:1336017158668554290>",
            "common": "<:commoncrate:1335016425827471491>",
            "uncommon": "<:uncommoncrate:1335016439085666408>",
            "rare": "<:rarecrate:1335016450381054155>",
            "epic": "<:epiccrate:1335016472044634242>",
            "legendary": "<:legendarycrate:1335016485134798888>"
        }
        user = await self.bot.database.connect_user(context.author.id)
        item = json.loads(user["item"])
        energy = json.loads(user["energy"])
        crate = json.loads(user["crate"])
        seed = random.randint(8, 32)
        seed2 = random.randint(2, 16)
        recovered = (energy["max"] - energy["energy"]) / energy["regen"]
        if energy["energy"] < seed:
            return await context.send(f"**Insufficient energy!** \nYour energy: **{energy['energy']}**, need **{seed}** energy for this action. \nFully recovered: **{round(recovered)} minute(s)** left.")
        energy["energy"] -= seed
        energy["regen_last"] = int(time.time())
        items = random.choice(["wood", "wheat", "steel", "trash", "stone"])
        rewards = {
            "item": random.randint(round(2 * seed * seed2 * user["level"] / 100), 5 + round(5 * seed * seed2 * user["level"] / 100)),
            "money": random.randint(round(50 * seed * seed2 * user["level"] / 100), 125 + round(125 * seed * seed2 * user["level"] / 100))
        }
        crate_m = None
        if random.random() < 0.1:
            crate_found = Utils.choice(crates)
            crate_m = f"- You found {crate_e[crate_found]} crate, type `.crate open` to open it.\n" 
            crate[crate_found] += 1
        user["money"] += rewards['money']
        item[items] += rewards["item"]
        embed = discord.Embed(
            description=(
                "You are strolling around and found:\n"
                f"- Money: {rewards['money']:,} <:rupiah:1334623817850552341>\n" 
                f"{crate_m if crate_m is not None else ''}"
                f"- {items.capitalize()}: {rewards['item']:,} {item_e[items]}\n"
                f"Consume {seed} energy."
            ), color=0xBEBEFE
        )
        user["item"] = json.dumps(item)
        user["energy"] = json.dumps(energy)
        user["crate"] = json.dumps(crate)
        await self.bot.database.update_user(context.author.id, user)
        embed.set_author(name="User Inventory")
        embed.set_footer(text=f"Requested by {context.author}.")
        await context.send(embed=embed) 

    @commands.hybrid_command(
        name="start",
        description="Start your journey with this bot."
    )
    async def start(self, context: Context) -> None:
        user = await self.bot.database.connect_user(context.author.id)
        chars = json.loads(user["character"])
        if len(chars) > 0:
            return await context.send(content="You're already registered, use `/rpg help <command>` if you feeling lost.")
        chars.append(Hero.Akira)
        chars.append(Hero.Josep)
        chars.append(Hero.Sigit)
        await context.send(content="New user added! Thanks for register, use `/rpg help <command>` if you feeling lost.\nSome characters have been added to you, see `/character list`")
        user["character"] = json.dumps(chars)
        await self.bot.database.update_user(context.author.id, user)
        return

    @commands.hybrid_command(
        name="character",
        description="Your character details."
    )
    async def character(self, context: Context, id: Optional[str] = None) -> None:
        user = await self.bot.database.connect_user(context.author.id)
        chars = json.loads(user["character"])

        if len(chars) <= 0:
            return await context.send(content="Seems like you're new, type `/start` to start your journey!")

        if id == "equip":
            return await self._handle_equip(context, chars)
        elif id == "unequip":
            return await self._handle_unequip(context, chars)
        elif id == "party":
            return await self._handle_party(context, chars)
        elif id is not None and Utils.find(id, chars, key="id") is not None:
            return await self._show_character_details(context, chars, id)
        else:
            return await self._show_character_list(context, chars)

    async def _show_character_details(self, context: Context, chars: list, id: str) -> None:
        data = Utils.find(id, chars, key="id")
        templates = {
            "detail": Messages.charDetailPage,
            "amp_res": Messages.amplificationResistancePage,
            "skills": Messages.skillPage,
            "story": Messages.storyPage
        }
        pagination = Interface.PaginationRPGCharDetail(context)
        pagination.create(data=data, template=templates)
        await pagination.start()

    async def _show_character_list(self, context: Context, chars: list) -> None:
        pagination = Interface.PaginationRPGCharList(context)
        pagination.create(data=chars, template=Messages.charListPage.strip())
        await pagination.start()

    async def _handle_equip(self, context: Context, chars: list) -> None:
        show = [char for char in chars if char["showdown"]]
        if len(show) >= 3:
            return await context.send(content="Your party is full, please unequip a character with `/character unequip`.")

        select = Interface.Select(context)
        view = select(
            message="Please select a character.",
            value=[
                (char["name"], char["id"], f"Choose to add {char['name']} to your party.", "📍") 
                for char in chars if not char["showdown"]
            ]
        )
        response = await view.show()
        selected = Utils.find(response.response, chars)
        chars = Utils.overwrite({"showdown": True}, chars, id=response.response)

        party_description = "\n".join(
            f"- {char['name']} `{char['class']}` *{char['element']}*" 
            for char in chars if char["showdown"]
        )
        embed = discord.Embed(
            description=(
                f"Successfully added **{selected['name']}** to your party.\n"
                "----------\n"
                "Your current party:\n"
                f"{party_description}"
            ),
            color=0xBEBEFE
        )
        user = await self.bot.database.connect_user(context.author.id)
        user["character"] = json.dumps(chars)
        await self.bot.database.update_user(context.author.id, user)
        await context.send(embed=embed)

    async def _handle_unequip(self, context: Context, chars: list) -> None:
        show = [char for char in chars if char["showdown"]]
        if len(show) == 0:
            return await context.send(content="Your party is empty. To add a character, type `/character equip`.")

        select = Interface.Select(context)
        view = select(
            message="Please select a character.",
            value=[
                (char["name"], char["id"], f"Choose to remove {char['name']} from your party.", "📍") 
                for char in chars if char["showdown"]
            ]
        )
        response = await view.show()
        selected = Utils.find(response.response, chars)
        chars = Utils.overwrite({"showdown": False}, chars, id=response.response)

        party_description = "\n".join(
            f"- {char['name']} `{char['class']}` *{char['element']}*" 
            for char in chars if char["showdown"]
        ) or "Your party is empty."
        embed = discord.Embed(
            description=(
                f"Successfully removed **{selected['name']}** from your party.\n"
                "----------\n"
                "Your current party:\n"
                f"{party_description}"
            ),
            color=0xBEBEFE
        )
        user = await self.bot.database.connect_user(context.author.id)
        user["character"] = json.dumps(chars)
        await self.bot.database.update_user(context.author.id, user)
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    async def _handle_party(self, context: Context, chars: list) -> None:
        party_description = "\n".join(
            f"- {char['name']} `{char['class']}` *{char['element']}*" 
            for char in chars if char["showdown"]
        ) or "Your party is empty."
        embed = discord.Embed(
            description=(
                "Your current party:\n"
                f"{party_description}"
            ),
            color=0xBEBEFE
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)
    
    @character.autocomplete('id')
    async def character_autocomplete(
        self, 
        interaction: discord.Interaction, 
        current: str
    ) -> List[app_commands.Choice[str]]:
        user = await self.bot.database.connect_user(interaction.user.id)
        chars = json.loads(user["character"])
        char_ids = [char["id"] for char in chars]
        return [
            app_commands.Choice(name=char_id, value=char_id)
            for char_id in char_ids if current.lower() in char_id.lower()
        ]


async def setup(bot) -> None:
    await bot.add_cog(RPG(bot))
