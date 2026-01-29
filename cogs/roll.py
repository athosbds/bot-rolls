import discord
from discord import app_commands
from discord.ext import commands
import random

RACAS = [
    ("Humano", "🟢 Comum", 35, "https://pin.it/4F79yqJc3"),
    ("Metahumano", "🟢 Comum", 20, "https://media.giphy.com/media/3o7TKz5e8aA5V8pEo0/giphy.gif"),
    ("Homo Magi", "🟢 Comum", 8, "https://media.giphy.com/media/26tknCqiJrBQG6DrG/giphy.gif"),
    ("Atlante", "🟢 Comum", 6, "https://pin.it/2IkeryQYW"),
    ("Androide", "🟢 Comum", 3.5, "https://media.giphy.com/media/3o7TKsQ8gTp3WqXq3q/giphy.gif"),
    ("Amazona", "🔵 Raro", 4, "https://media.giphy.com/media/l0MYJz7qYq2Xq6q7S/giphy.gif"),
    ("Thanagariano", "🔵 Raro", 4, "https://media.giphy.com/media/3o7TKz4kX8jvqJvJq0/giphy.gif"),
    ("Ranniano", "🔵 Raro", 3, "https://media.giphy.com/media/l0MYJv9q9k8k8k8k8/giphy.gif"),
    ("Coluano", "🔵 Raro", 3, "https://media.giphy.com/media/3o7TKz7yv9yv9yv9y/giphy.gif"),
    ("Apokoliptiano", "🔵 Raro", 3, "https://media.giphy.com/media/l0MYJv9q9k8k8k8k8/giphy.gif"),
    ("Tamaraniano", "🟣 Épico", 3, "https://pin.it/2ptdD8mmY"),
    ("Marciano Verde", "🟣 Épico", 2, "https://media.giphy.com/media/l0MYJv9q9k8k8k8k8/giphy.gif"),
    ("Marciano Branco", "🟣 Épico", 2, "https://media.giphy.com/media/3o7TKz7yv9yv9yv9y/giphy.gif"),
    ("Daxamita", "🔴 Lendário", 1.5, "https://media.giphy.com/media/l0MYJv9q9k8k8k8k8/giphy.gif"),
    ("Kryptoniano", "🔴 Lendário", 1, "https://pin.it/7wqLEYGtt"),
    ("Novo Deus", "⚫ Mítico", 0.5, "https://media.giphy.com/media/l0MYJv9q9k8k8k8k8/giphy.gif"),
]

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Sorteia uma raça aleatória da DC")
    async def roll(self, interaction: discord.Interaction):
        pesos = [r[2] for r in RACAS]
        raca_sorteada = random.choices(RACAS, weights=pesos, k=1)[0]
        nome, raridade, chance, gif_url = raca_sorteada

        embed = discord.Embed(
            title="🎲 **RAÇA SORTEADA** 🎲",
            description=f"**{nome}**",
            color=self._get_color_by_rarity(raridade)
        )
        embed.add_field(name="⭐ **Raridade**", value=raridade, inline=True)
        embed.add_field(name="📊 **Chance**", value=f"{chance}%", inline=True)
        embed.set_image(url=gif_url)
        embed.set_footer(text=f"Sorteado para {interaction.user.display_name}", 
                        icon_url=interaction.user.avatar.url if interaction.user.avatar else None)

        await interaction.response.send_message(embed=embed)

    def _get_color_by_rarity(self, rarity: str) -> discord.Color:
        colors = {
            "🟢 Comum": discord.Color.green(),
            "🔵 Raro": discord.Color.blue(),
            "🟣 Épico": discord.Color.purple(),
            "🔴 Lendário": discord.Color.red(),
            "⚫ Mítico": discord.Color.dark_gray(),
        }
        return colors.get(rarity, discord.Color.random())

async def setup(bot):
    await bot.add_cog(Roll(bot))