import os
import nextcord
from nextcord.ext import commands

from scheduler import scheduler_loop
from storage import add_monitor, remove_monitor
from instagram import check_instagram_status
import keepalive

TOKEN = os.getenv("DISCORD_TOKEN")

intents = nextcord.Intents.default()
bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    keepalive.start()

    async def monitor_task(monitor):
        try:
            active = await check_instagram_status(monitor["username"])
        except Exception as e:
            print("❌ Instagram error:", e)
            return

        channel = bot.get_channel(monitor["channel_id"])
        if not channel:
            return

        if monitor["status"] == "unknown":
            monitor["status"] = "active" if active else "inactive"
            return

        if active and monitor["status"] == "inactive":
            await channel.send(f"🟢 **@{monitor['username']} reactivated**")
            monitor["status"] = "active"

        elif not active and monitor["status"] == "active":
            await channel.send(f"🔴 **@{monitor['username']} deactivated**")
            monitor["status"] = "inactive"

    bot.loop.create_task(scheduler_loop(monitor_task))

@bot.slash_command(description="Start monitoring an Instagram account")
async def monitor(interaction, username: str, interval: int):
    if interval < 60:
        await interaction.response.send_message(
            "⚠️ Interval must be at least 60 seconds",
            ephemeral=True
        )
        return

    add_monitor(
        interaction.user.id,
        interaction.channel.id,
        username,
        interval
    )

    await interaction.response.send_message(
        f"📡 Monitoring **@{username}** every **{interval}s**"
    )

@bot.slash_command(description="Stop monitoring an Instagram account")
async def unmonitor(interaction, username: str):
    if remove_monitor(interaction.user.id, username):
        await interaction.response.send_message(
            f"❌ Stopped monitoring **@{username}**"
        )
    else:
        await interaction.response.send_message(
            "⚠️ Monitor not found"
        )

@bot.slash_command(description="Ping bot")
async def ping(interaction):
    await interaction.response.send_message("🏓 Bot is alive!")

bot.run(TOKEN)
