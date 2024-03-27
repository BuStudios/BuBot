import discord
import common.reminder_db as reminder_db
from discord.ui.item import Item

class ReminderView(discord.ui.View):
    def __init__(self, user_reminders):
        super().__init__()
        self.select_menu = discord.ui.Select(placeholder="Select a reminder to cancel", min_values=1, max_values=1)

        for reminder in user_reminders:
            self.select_menu.add_option(label=reminder["reminder_id"], description=reminder["reason"], value=reminder["reminder_id"])
            
        self.select_menu.callback = self.select_callback
        self.add_item(self.select_menu)

    async def select_callback(self, interaction: discord.Interaction):
        deletion = reminder_db.delete_reminder(self.select_menu.values[0])
        if deletion == "success":
            await interaction.response.send_message(f"✅ The reminder `{self.select_menu.values[0]}` has been canceled!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Could not find the reminder to delete!", ephemeral=True)

class CancelButton(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="Cancel Reminder", style=discord.ButtonStyle.danger)
    async def button_callback(self, button, interaction):
        if interaction.user.id == self.user_id:

            button.disabled = True
            await interaction.response.edit_message(view=self)

            await interaction.followup.send("✅ Canceled Reminder!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ You can't cancel someone elses reminder!", ephemeral=True)