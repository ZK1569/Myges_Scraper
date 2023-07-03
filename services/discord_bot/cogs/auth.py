from discord.ext import commands
import mongo

class Auth(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = mongo.MongoConnect()

    @commands.command()
    async def save(self, ctx, GesId=None, password=None):
        """
            Save your myGes id and password
            Saves the user's information in a database for scrapping his MyGes account.
        """

        user_id = ctx.author.id

        # Check if the user has already saved this information 
        if self.db.isUserSaved(user_id):
            await ctx.send("Your information is already saved.\nIf you want to change your password, you can do : \n`!changepassword <YOUR NEW PASSWORD>`")
            return 
        
        # Checks that the user has sent an id and password 
        if not GesId or not password:
            await ctx.send("You forgot to send me your mygGes Id and password")
            return 

        isSaved = self.db.saveLogin(user_id, GesId, password)

        if(isSaved):
            await ctx.send("Thanks for the personal info ...")
            return
        
        await ctx.send("I'm so stupid... I couldn't save the information.")
        return

    @commands.command()
    async def bye(self, ctx):
        """
            Delete your myGes id and password
        """

        user_id = ctx.author.id

        # Check if the user has already saved his information 
        if not self.db.isUserSaved(user_id):
            await ctx.send("I don't know your myGes Id and password")
            return 

        # Delete informations
        # If the response of the function is true or false 
        if self.db.deleteLogin(user_id):
            await ctx.send("Okay, I'll never use that information again")
            return 


        await ctx.send("I haven't been able to forget your information ")
        return 
    
    @commands.command()
    async def me(self, ctx):
        """
            Show your informations

            Enables you to check whether the user who executes the order has his myGes ID and password saved in the database.
        """
        user_id = ctx.author.id
        user_name = ctx.author.name

        message = f"Your are **{user_name}** and your ID is **{user_id}** \n \n"
        if(self.db.isUserSaved(user_id)):
            message += "And I know your myges password and id"
        else:
            message += f"I don't know your password and myGes ID \nYou can do the cmd `!save <YOUR ID> <PASSWORD>`"

        await ctx.send(message)

    @commands.command(
        hidden=True
    )
    async def changepassword(self, ctx, password):
        """
            This command changes the password
        """

        await ctx

async def setup(bot):
    await bot.add_cog(Auth(bot))