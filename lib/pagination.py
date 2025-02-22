import json
import discord
from discord.ext import commands
from typing import List, Dict, Any, Optional

class toProperty:
    def __init__(self, data: dict):
        self.__dict__.update(data)

    def dict(self):
        return self.__dict__.copy()

class PaginationRPGCharList(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)  
        self.ctx = ctx
        self.data: List[Dict[str, Any]] = []
        self.template: str = ""
        self.index = 0

    def create(self, data: List[Dict[str, Any]], template: str):
        self.data = data
        self.template = template

    def format_template(self, character: Dict[str, Any]) -> str:
        char = toProperty(character)
        stats = toProperty(character["stats"])
        cdm = int(stats.Crit_DMG * 100)
        cdr = int(stats.Crit_Rate * 100)

        return self.template.format(char=char, stats=stats, cdm=cdm, cdr=cdr)

    async def start(self):
        if not self.data:
            return await self.ctx.send("No character data available.")

        embed = discord.Embed(
            description=self.format_template(self.data[self.index]), 
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"Viewing --- Page {self.index + 1} of {len(self.data)}")

        self.update_buttons() 
        await self.ctx.send(embed=embed, view=self)

    async def update_message(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description=self.format_template(self.data[self.index]), 
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"Viewing --- Page {self.index + 1} of {len(self.data)}")

        self.update_buttons()  
        await interaction.response.edit_message(embed=embed, view=self)

    def update_buttons(self):
        self.previous.style = discord.ButtonStyle.red if self.index == 0 else discord.ButtonStyle.blurple
        self.previous.disabled = self.index == 0

        self.next.style = discord.ButtonStyle.red if self.index == len(self.data) - 1 else discord.ButtonStyle.blurple
        self.next.disabled = self.index == len(self.data) - 1

    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        if self.index > 0:
            self.index -= 1
            await self.update_message(interaction)

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        if self.index < len(self.data) - 1:
            self.index += 1
            await self.update_message(interaction)


class PaginationRPGCharDetail(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.data: Dict[str, Any] = {}
        self.templates: Dict[str, str] = {}
        self.pages: List[discord.Embed] = []
        self.index = 0

    def create(self, data: Dict[str, Any], template: Dict[str, str]):
        self.data = data
        self.templates = template
        self.pages = [
            self.get_status_page(),
            self.get_amplification_resistance_page(),
            self.get_skill_page(page=1),
            self.get_skill_page(page=2),
            self.get_story_page()
        ]

    def get_status_page(self) -> discord.Embed:
        char = toProperty(self.data)
        stats = toProperty(self.data["stats"])
        embed = discord.Embed(
            description=self.templates["detail"].format(
                char=char,
                stats=stats,
                cdm=int(stats.Crit_DMG * 100),
                cdr=int(stats.Crit_Rate * 100),
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Viewing --- Page 1 of 5")
        return embed

    def get_amplification_resistance_page(self) -> discord.Embed:
        char = toProperty(self.data)
        amp = toProperty(self.data["amplification"])
        res = toProperty(self.data["resistance"])
        embed = discord.Embed(
            description=self.templates["amp_res"].format(
                char=char,
                amp=amp,
                res=res
            ),
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Viewing --- Page 2 of 5")
        return embed

    def get_skill_page(self, page: int) -> discord.Embed:
        char = self.data
        chara = toProperty(self.data)
        skills_text = []

        # Determine the range of skills to display based on the page number
        skills_range = char["skills"][:2] if page == 1 else char["skills"][2:]

        for skill in skills_range:
            if skill["type"] == "attack":
                percentage = int(skill.get("ATK", 0) * 100)
                mess = (
                    f"🔹 **{skill['name']}**\n"
                    f"- *Type:* {skill['type'].capitalize()}\n"
                    f"- *Level:* {skill['level']}\n"
                    f"- *Description:* {skill['description'].replace('{percentage}', str(percentage))}\n"
                )
            else:
                percentage = int(skill[skill["main"]] * 100)
                addition = ""
                if skill["status"] == "buff":
                    buff = skill["buff"]
                    percentage = int(buff[buff[buff["type"]][0]] * 100)
                    addition = f"- *Buff:* {buff['name']} for {buff['turn']} turn(s)\n"
                elif skill["status"] == "debuff":
                    debuff = skill["debuff"]
                    percentage = int(debuff[debuff[debuff["type"]][0]] * 100)
                    addition = f"- *Debuff:* {debuff['name']} for {debuff['turn']} turn(s)\n"
                elif skill["status"] == "dot":
                    debuff = skill["debuff"]
                    percentage = int(debuff["ATK"] * 100)
                    addition = f"- *DoT:* {debuff['name']} for {debuff['turn']} turn(s)\n"

                mess = (
                    f"🔹 **{skill['name']}** `{skill['status'].upper()}`\n"
                    f"- *Type:* {skill['type'].capitalize()} Skill\n"
                    f"- *Level:* {skill['level']}\n"
                    f"- *Cost:* {skill['cost']} Mana\n"
                    f"- *Effect:* {skill['description'].replace('{percentage}', str(percentage))}\n"
                    + addition
                )
            skills_text.append(mess)

        embed = discord.Embed(
            description=self.templates["skills"].format(
                char=chara,
                skills="\n".join(skills_text)
            ),
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Viewing --- Page {page + 2} of 5")
        return embed

    def get_story_page(self) -> discord.Embed:
        char = toProperty(self.data)
        story = toProperty(self.data["story"])
        embed = discord.Embed(
            description=self.templates["story"].format(char=char, story=story),
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"Viewing --- Page 5 of 5")
        return embed

    async def start(self):
        embed = self.pages[self.index]
        self.update_buttons()
        await self.ctx.send(embed=embed, view=self)

    async def update_message(self, interaction: discord.Interaction):
        embed = self.pages[self.index]
        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)

    def update_buttons(self):
        self.previous.disabled = self.index == 0
        self.next.disabled = self.index == len(self.pages) - 1

        self.previous.style = discord.ButtonStyle.red if self.previous.disabled else discord.ButtonStyle.blurple
        self.next.style = discord.ButtonStyle.red if self.next.disabled else discord.ButtonStyle.blurple

    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        if self.index > 0:
            self.index -= 1
            await self.update_message(interaction)

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        if self.index < len(self.pages) - 1:
            self.index += 1
            await self.update_message(interaction)