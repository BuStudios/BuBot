import discord
import common.reminder_db as reminder_db
import common.views
import common.emojis

async def reminder_list(ctx):
    user_reminders, reminder_count = reminder_db.get_user_reminders(ctx.author.id)

    if reminder_count == 0:
        await ctx.respond(f"{common.emojis.no} You don't have any active reminders!", ephemeral=True)
    else:
        embed = discord.Embed(title="Your reminders")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

        reminder_text = "\n".join([f"🔔 `({reminder['reminder_id']})` **{reminder['reason']}** <t:{reminder['timestamp']}:R>" for reminder in user_reminders])

        embed.add_field(name="", value=reminder_text)

        embed.set_footer(text=f"You have {reminder_count} active reminders")

        view = common.views.ReminderView(user_reminders)

        await ctx.respond(embed=embed, ephemeral=True, view=view)