import discord
from discord.ext import commands

from core.bot import Bot
from commands.ui.CaptchaCommandUI import SetChannelButton, SetRoleButton
from commands.ui.ModuleView import ModuleView
from commands.core.Context import Context
from commands.core.Checks import whitelistOnly
from modules.Captcha import Captcha
from util.EmbedUtils import EmbedUtils


def captchaEmbed(captcha: Captcha):

    em = EmbedUtils.basicEmbed(
        title="Captcha",
        description="> Captcha module prevents your server from self-bots by sending a captcha verification to each new "
                    "user on your server !\n"
                    "⚠️ **Warning:** captcha verification won't be send if the channel or the role is invalid !"
    )
    em.add_field(
        name="Enabled:",
        value="<:check:1112014748310065202>" if captcha.enabled else "<:cross:1112014825447510109>"
    )
    em.add_field(
        name="Channel:",
        value=f"<#{captcha.channelID}>" if captcha.channelID is not None else "Not defined yet !"
    )
    em.add_field(
        name="Role:",
        value=f"<@&{captcha.roleID}>" if captcha.roleID is not None else "Not defined yet !"
    )

    return em


class CaptchaCommand(commands.Cog):

    @whitelistOnly()
    @discord.guild_only()
    @discord.slash_command(name="captcha")
    async def _captcha(self, ctx: Context):

        await ctx.response.defer(ephemeral=True)

        captcha = ctx.bot.getInstance(ctx.guild_id, Captcha)

        captchaView = ModuleView(ctx.bot, captcha, captcha)
        captchaView.add_item(SetChannelButton(ctx.bot, captchaEmbed))
        captchaView.add_item(SetRoleButton(ctx.bot, captchaEmbed))

        await ctx.send_followup(
            embed=captchaEmbed(captcha),
            view=captchaView
        )


def setup(bot: Bot):

    bot.add_cog(CaptchaCommand())
