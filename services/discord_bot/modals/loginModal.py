import discord
import mongo

class LoginModal(discord.ui.Modal, title="What is your myGes login"):

    lm_login = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Login",
        required=True,
        placeholder="Your login"
    )

    lm_password = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Password",
        required=True,
        placeholder="Your password"
    )

    async def on_submit(self, interaction: discord.Interaction):
        db = mongo.MongoConnect() # <---- TODO: Change this shit

        user_id = interaction.user.id
        GesId = self.lm_login.value
        password = self.lm_password.value

        if db.isUserSaved(user_id):
            await interaction.response.send_message("Your information is already saved.\nIf you want to change your password, you can do : \n`!changepassword <YOUR NEW PASSWORD>`")
            return 

        status = db.saveLogin(user_id, GesId, password)

        if status:
            await interaction.response.send_message("Thanks for the personal info ...")
        else:
            await interaction.response.send_message("c'est de la merde ")

    async def on_error(self, interaction: discord.Interaction, error):
        # TODO:
        pass
