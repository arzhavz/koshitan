import discord
import asyncio
from typing import List, Set

class Select:
    def __init__(self, ctx: discord.ext.commands.Context):
        self.ctx = ctx
        self.response = None

    class Dropdown(discord.ui.Select):
        def __init__(self, options, parent):
            self.parent = parent
            select_options = [
                discord.SelectOption(label=label, value=value, description=desc, emoji=emoji)
                for label, value, desc, emoji in options
            ]
            super().__init__(placeholder="Choose an option ...", options=select_options)

        async def callback(self, interaction: discord.Interaction):
            self.parent.response = interaction.data["values"][0]
            await interaction.response.defer()
            self.view.stop()  

    async def show(self):
        view = discord.ui.View()
        dropdown = self.Dropdown(self.options, self)
        view.add_item(dropdown)

        message = await self.ctx.send(content=self.message, view=view)

        try:
            await asyncio.wait_for(view.wait(), timeout=30.0)

            if self.response is None:
                await message.edit(content="Timed out!", view=None)
                return None

            await message.delete()
            return self

        except asyncio.TimeoutError:
            if self.response is None:
                await message.edit(content="Timed out!", view=None)
                return None
            else:
                await message.delete()
                return self

    def __call__(self, message: str, value: List[Set[str]]):
        """
        Create Select.
        """
        self.message = message
        self.options = value
        return self

class Button:
    class CustomButtonView(discord.ui.View):
        def __init__(self, user_id: int, values: list, style: discord.ButtonStyle = discord.ButtonStyle.blurple):
            super().__init__()
            self.user_id = user_id
            self.selected_value = None  

            for label, val in values:
                self.add_item(self.Button(label, val, self, style))

        async def interaction_check(self, interaction: discord.Interaction) -> bool:
            return interaction.user.id == self.user_id

        async def wait(self):
            await super().wait()

        def value(self):
            return self.selected_value  

        class Button(discord.ui.Button):
            def __init__(self, label, val, parent, style):
                super().__init__(label=label, style=style)
                self.val = val
                self.parent = parent

            async def callback(self, interaction: discord.Interaction):
                self.parent.selected_value = self.val
                self.parent.stop()

    def __init__(self, user: discord.User):
        self.user_id = user.id

    def create(self, values: list, style: discord.ButtonStyle = discord.ButtonStyle.blurple):
        return self.CustomButtonView(self.user_id, values, style)

class Misc:
    def progress_bar(nilai, nilai_max, length=40):
        """
        Menampilkan progress bar sebagai teks.

        :param nilai: Nilai saat ini
        :param nilai_max: Nilai maksimum
        :param length: Panjang progress bar (default 40)
        """
        percent = (nilai / nilai_max)
    
        bar_length = int(length * percent)
        bar = '=' * bar_length + '-' * (length - bar_length)
    
        return f'[{bar}] {percent * 100:.2f}%'