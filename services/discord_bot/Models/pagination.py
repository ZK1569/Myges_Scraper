import discord

class PaginationStudentView(discord.ui.View):

    current_page: int = 1
    sep: int = 1
    
    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        embed = discord.Embed(
            color=discord.Color.blue()
            )
        for item in data:

            embed.set_footer(text=f"{self.current_page}/{len(self.data)}")
            embed.add_field(name=item.last_name, value=item.first_name, inline=False)
            embed.set_image(url=item.image)
        return embed
    
    def update_buttons(self):
        if self.current_page <= 1:
            self.prev_button.disabled = True
        else:
            self.prev_button.disabled = False

        if self.current_page >= len(self.data):
            self.next_button.disabled = True
        else:
            self.next_button.disabled = False

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    @discord.ui.button(emoji="⬅️")
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item: until_item])

    @discord.ui.button(emoji="➡️")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        await self.update_message(self.data[from_item: until_item])
