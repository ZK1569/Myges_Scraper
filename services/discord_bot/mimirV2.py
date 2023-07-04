import settings
import discord 
from discord.ext import commands
from Modals.LoginModal import LoginModal

logger = settings.logging.getLogger("Bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)

        # Load all the commands (for the moment there is no commands)
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
            logger.error(error)
            return 
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument")
            logger.error(error)
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


    # Slash commands ------------------------------------------------
    @bot.tree.command()
    async def login(interaction: discord.Interaction):
        login_model = LoginModal()
        await interaction.response.send_modal(login_model)
        

    # Admin commands ------------------------------------------------
    @bot.command(hidden=True)
    @commands.is_owner()
    async def load(ctx, cog:str):
        await bot.load_extension(f"cogs.{cog.lower()}")
        logger.warning(f"{cog} is loaded")

    @bot.command(hidden=True)
    @commands.is_owner()
    async def reload(ctx, cog:str):
        await bot.reload_extension(f"cogs.{cog.lower()}")
        logger.warning(f"{cog} is reloaded")

    @bot.command(hidden=True)
    @commands.is_owner()
    async def unload(ctx, cog:str):
        await bot.unload_extension(f"cogs.{cog.lower()}")
        logger.warning(f"{cog} is unloaded")


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()