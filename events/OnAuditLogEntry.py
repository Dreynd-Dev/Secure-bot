from discord import AuditLogEntry, AuditLogAction, Member
from discord.ext import commands

from core.Bot import Bot
from modules.AntiNuke import AntiNuke


class OnAuditLogEntry(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot: Bot = bot
        self.triggerActions: list[AuditLogAction] = [
            AuditLogAction.channel_create,
            AuditLogAction.channel_update,
            AuditLogAction.channel_delete,
            AuditLogAction.webhook_create,
            AuditLogAction.webhook_update,
            AuditLogAction.webhook_delete,
            AuditLogAction.role_create,
            AuditLogAction.role_update,
            AuditLogAction.role_delete,
            AuditLogAction.kick,
            AuditLogAction.ban,
            AuditLogAction.unban,
            AuditLogAction.bot_add
        ]

    @commands.Cog.listener("on_audit_log_entry_create")
    async def on_audit_log_entry_create(self, entry: AuditLogEntry):

        if entry.action in self.triggerActions:

            antiNuke: AntiNuke = self.bot.getModuleInstance(entry.guild.id, AntiNuke)

            if antiNuke.enabled:

                member: Member = entry.guild.get_member(entry.user.id)

                if member is not None:

                    await antiNuke.new_element(member)


async def setup(bot: Bot):

    await bot.add_cog(OnAuditLogEntry(bot))
