import discord
from discord.ext import commands
import os
import random
from flask import Flask
from threading import Thread
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 DC Roll Bot Online 24/7 no Render!"

@app.route('/health')
def health():
    return "OK", 200

def run_webserver():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("Token do Discord não encontrado!")

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

RACAS = [
    ("Humano", "🟢 Comum", 35),
    ("Metahumano", "🟢 Comum", 20),
    ("Homo Magi", "🟢 Comum", 8),
    ("Atlante", "🟢 Comum", 6),
    ("Androide", "🟢 Comum", 3.5),
    ("Amazona", "🔵 Raro", 4),
    ("Thanagariano", "🔵 Raro", 4),
    ("Ranniano", "🔵 Raro", 3),
    ("Coluano", "🔵 Raro", 3),
    ("Apokoliptiano", "🔵 Raro", 3),
    ("Tamaraniano", "🟣 Épico", 3),
    ("Marciano Verde", "🟣 Épico", 2),
    ("Marciano Branco", "🟣 Épico", 2),
    ("Daxamita", "🔴 Lendário", 1.5),
    ("Kryptoniano", "🔴 Lendário", 1),
    ("Novo Deus", "⚫ Mítico", 0.5),
]

@bot.tree.command(name="roll", description="Sorteia uma raça da DC")
async def roll(interaction: discord.Interaction):
    pesos = [r[2] for r in RACAS]
    raca_sorteada = random.choices(RACAS, weights=pesos, k=1)[0]
    nome, raridade, chance = raca_sorteada
    
    cores = {
        "🟢 Comum": discord.Color.green(),
        "🔵 Raro": discord.Color.blue(),
        "🟣 Épico": discord.Color.purple(),
        "🔴 Lendário": discord.Color.red(),
        "⚫ Mítico": discord.Color.dark_gray(),
    }
    
    embed = discord.Embed(
        title="🎲 RAÇA SORTEADA 🎲",
        description=f"**{nome}**",
        color=cores.get(raridade, discord.Color.random())
    )
    embed.add_field(name="⭐ Raridade", value=raridade, inline=True)
    embed.add_field(name="📊 Chance", value=f"{chance}%", inline=True)
    embed.set_footer(text=f"Sorteado para {interaction.user.name}")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Verificar latência do bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comandos sincronizados")
    except Exception as e:
        print(f"Erro ao sincronizar: {e}")

def start_bot():
    bot.run(TOKEN)

if __name__ == "__main__":
    webserver_thread = Thread(target=run_webserver, daemon=True)
    webserver_thread.start()
    start_bot()