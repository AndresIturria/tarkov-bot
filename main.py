import discord
from discord.ext import commands
import utilities
import models.leaderboard


if __name__ == '__main__':
    bot = commands.Bot(command_prefix="¿")
    TOKEN = utilities.load_token()

    @bot.command(
        help="",
        brief=""
    )
    async def killed(ctx, *args):
        if len(args) > 2 or len(args) == 0:
            await ctx.channel.send("error")

        else:
            killer_id = utilities.parse_userid(args[0])
            killed_id = utilities.parse_userid(args[1])
            server_id = ctx.guild.id
            models.leaderboard.add_killed(server_id, killer_id, killed_id)
            await ctx.channel.send("Done")


    @bot.command(
        help="",
        brief=""
    )
    async def leaderboard(ctx):
        leaderboard_doc = models.leaderboard.get_leaderboard(ctx.guild.id)

        for killer in leaderboard_doc:
            killer_member = await ctx.guild.fetch_member(killer["killer_id"])
            killer_name = killer_member.display_name
            embed = discord.Embed(title=killer_name, color=0x03f8fc)

            for user in killer["killed"]:
                member = await ctx.guild.fetch_member(user)
                embed.add_field(name=member.display_name, value=killer["killed"][user])

            embed.add_field(name="Total", value=killer["total"])
            await ctx.channel.send(embed=embed)


    @bot.command(
        help="",
        brief=""
    )
    async def find(ctx, *args):
        if len(args) > 1 or len(args) == 0:
            await ctx.channel.send("error")

        else:
            killer_id = utilities.parse_userid(args[0])
            killer_member = await ctx.guild.fetch_member(killer_id)
            killer_name = killer_member.display_name
            embed = discord.Embed(title=killer_name, color=0x03f8fc)

            killer = models.leaderboard.get_killer(ctx.guild.id, killer_id)

            for user in killer["killed"]:
                member = await ctx.guild.fetch_member(user)
                embed.add_field(name=member.display_name, value=killer["killed"][user])

            embed.add_field(name="Total", value=killer["total"])
            await ctx.channel.send(embed=embed)


    @bot.event
    async def on_ready():
        print('Online')

    bot.run(TOKEN)
