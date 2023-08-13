import discord
from discord.ext import commands

from core.bot import Bot
from util.EmbedUtils import EmbedUtils
from commands.core.Checks import ownerOnly, whitelistOnly


class WhitelistCommands(commands.Cog):

    def __init__(self, bot: Bot):

        self.bot: Bot = bot

    wl = discord.SlashCommandGroup("whitelist")

    @ownerOnly()
    @discord.guild_only()
    @wl.command(name="add")
    async def _wl_add(self, ctx: discord.ApplicationContext, member: discord.Member):

        await ctx.response.defer(ephemeral=True)

        guildData: dict = ctx.bot.file.getGuildData(ctx.guild_id)

        if member.id not in guildData["whitelist"]:

            guildData["whitelist"].append(member.id)
            await ctx.bot.file.updateGuildData(ctx.guild_id, guildData)

            em: discord.Embed = EmbedUtils.basicEmbed(
                title="Success !",
                description=member.mention + " has been successfully added to the whitelist !"
            )

            await ctx.send_followup(embed=em)

        else:

            em: discord.Embed = EmbedUtils.basicEmbed(
                title="Error !",
                description=member.mention + " is already in the whitelist !"
            )

            await ctx.send_followup(embed=em)

    @ownerOnly()
    @discord.guild_only()
    @wl.command(name="remove")
    async def _wl_rm(self, ctx: discord.ApplicationContext, member: discord.Member):

        await ctx.response.defer(ephemeral=True)

        guildData: dict = ctx.bot.file.getGuildData(ctx.guild_id)

        if member.id in guildData["whitelist"]:

            guildData["whitelist"].remove(member.id)
            await ctx.bot.file.updateGuildData(ctx.guild_id, guildData)

            em: discord.Embed = EmbedUtils.basicEmbed(
                title="Success !",
                description=member.mention + " has been successfully removed from the whitelist"
            )

            await ctx.send_followup(embed=em)

        else:

            em: discord.Embed = EmbedUtils.basicEmbed(
                title="Error !",
                description=member.mention + " is not in the whitelist !"
            )

            await ctx.send_followup(embed=em)

    @whitelistOnly()
    @discord.guild_only()
    @wl.command(name="see")
    async def _wl_see(self, ctx: discord.ApplicationContext):

        await ctx.response.defer(ephemeral=True)

        guildData = ctx.bot.file.getGuildData(ctx.guild_id)

        if guildData["whitelist"]:

            formatted_ids: list[str] = [f"<@{userID}>" for userID in guildData["whitelist"]]
            wl_members = ", ".join(formatted_ids)

        else:

            wl_members = "Actually, no one is in the whitelist !"

        em: discord.Embed = EmbedUtils.basicEmbed(
            title="Whitelist",
            description="> Whitelist is the list of members allowed to perform modifications to the bot parameters."
                        "Members in this list must be confidence member !\n"
                        "> **Note:** whitelisted members will be ignored by every protection systems !"
        )
        em.add_field(
            name="Members:",
            value=wl_members
        )

        await ctx.send_followup(embed=em)


def setup(bot: Bot):

    bot.add_cog(WhitelistCommands(bot))
