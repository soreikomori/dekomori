from discord.ext import commands

class InteractionHelpCommand(commands.DefaultHelpCommand):
    async def send_pages(self) -> None:
        if interaction := self.context.interaction:
            await interaction.response.defer()
            for page in self.paginator.pages:
                await interaction.followup.send(page)
            return
        destination = self.get_destination()
        for page in self.paginator.pages:
            await destination.send(page)