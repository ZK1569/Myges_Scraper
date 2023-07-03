# from discord.ext import commands

# @commands.group(adliases=["admin"])
# @commands.is_owner()
# async def admin(ctx):
#     if ctx.invoked_subcommand is None:
#         await ctx.send("Invalid admin command passed")

# @admin.command(hidden=True)
# async def load(ctx, cog:str):
#     await bot.load_extension(f"cogs.{cog.lower()}")

# @admin.command(hidden=True)
# async def reload(ctx, cog:str):
#     await bot.reload_extension(f"cogs.{cog.lower()}")

# @admin.command(hidden=True)
# async def unload(ctx, cog:str):
#     await bot.unload_extension(f"cogs.{cog.lower()}")
