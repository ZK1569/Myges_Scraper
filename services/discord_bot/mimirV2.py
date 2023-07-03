import settings
import discord 
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():

        # Load all the commands
        # for cmd_file in settings.CMDS_DIR.glob("*.py"):
        #     if cmd_file.name != "__init__.py":
        #         await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")

        # Load all the cogs
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")

        logger.info(f"{bot.user} is ready")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found")
            return 
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
            return 
        else:
            await ctx.send("Something went wrong")
            logger.error(error)

    @bot.command()
    async def ping(ctx):
        """
            Health check         
        """
        await ctx.send("pong")

    @bot.command(hidden=True)
    @commands.is_owner()
    async def load(ctx, cog:str):
        await bot.load_extension(f"cogs.{cog.lower()}")

    @bot.command(hidden=True)
    @commands.is_owner()
    async def reload(ctx, cog:str):
        await bot.reload_extension(f"cogs.{cog.lower()}")

    @bot.command(hidden=True)
    @commands.is_owner()
    async def unload(ctx, cog:str):
        await bot.unload_extension(f"cogs.{cog.lower()}")


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()