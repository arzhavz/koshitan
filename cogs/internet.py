import discord
import random

from discord.ext import commands
from discord.ext.commands import Context

from scraper.poop import Poop
from scraper.wallpaper import Wallpapers


class Internet(commands.Cog, name="internet"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="wallpaper",
        description="This command sends an epic wallpaper.",
        aliases=["wp"]
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wallpaper(self, context: Context, query: str) -> None:
        """
        This command sends an epic wallpaper from https://wallpapers.com

        :param context: The context of the command.
        :query: The query of the wallpaper.
        """
        try:
            url: str = Wallpapers(query)
            if not url:
                await context.send(f"Wallpaper not found")
                return
            image = random.choice(url)
            embed = discord.Embed(
                description="Here's your epic wallpaper!",
                color=0x4B36E3,
            )
            embed.set_author(name="Wallpaper Search")
            embed.set_image(url=image["url"])
            embed.add_field(name="ID:", value=image["id"], inline=True)
            embed.add_field(name="Title:", value=image["title"], inline=True)
            embed.add_field(name="Description:", value=image["desc"], inline=False)
            embed.add_field(name="Source:", value=image["page"], inline=False)
            embed.set_footer(text=f"Requested by {context.author}.")
            message = await context.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❎")
        except Exception as e:
            await context.send(f"Failed to send image: {e}")

    @commands.hybrid_command(
        name="poop",
        description="This command sends an epic poop video."
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def poop(self, context: Context, link: str) -> None:
        """
        Sends an epic video link from Poop.

        :param context: The command context.
        :param link: The Poop video URL.
        """
        try:
            message = await context.send("⏳ Please wait.")
            poop_data = Poop(link).content

            if not poop_data or poop_data.get("status") == "false":
                return await message.edit(content="❌ Video not found.")

            embed = discord.Embed(
                description=poop_data.get("title", "Untitled Video"),
                color=0x4B36E3,
            )
            embed.set_author(name="Poop Downloader")
            embed.set_footer(text=f"Requested by {context.author}")

            class SimpleView(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=15) 
                    self.message = None 
                    button = discord.ui.Button(
                        label=poop_data.get("message", "Watch Video"),
                        style=discord.ButtonStyle.url,
                        url=poop_data.get("link", "#")
                    )
                    self.add_item(button)

                async def on_timeout(self):
                    if self.message:
                        try:
                            await self.message.edit(content="Link timed out.", embed=None, view=None)
                        except discord.NotFound:
                            pass
                    await super().on_timeout()  

            view = SimpleView()
            await message.edit(content="✅ Success, message will removed after 15s.", embed=embed, view=view)
            view.message = message  

        except Exception as e:
            await message.edit(content=f"⚠️ An error occurred: `{e}`")


async def setup(bot) -> None:
    await bot.add_cog(Internet(bot))
