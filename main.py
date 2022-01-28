import discord
from discord.ext import commands
import utilities
import models.leaderboard


if __name__ == '__main__':

    async def get_discord_username(ctx, id):
        try:
            killer_member = await ctx.guild.fetch_member(id)
            return killer_member.display_name
        except(discord.errors.NotFound):
            return("This user is not in the server")



    bot = commands.Bot(command_prefix="¿")
    TOKEN = utilities.load_token()

    @bot.command(
        help="¿killed @killer @killed  add a teamkill to the count",
        brief="¿killed @killer @killed  add a teamkill to the count"
    )
    async def killed(ctx, *args):
        if len(args) > 2 or len(args) == 0 or args[0] == "@everyone" or args[1] == "@everyone":
            await ctx.channel.send("error")

        else:
            killer_id = utilities.parse_userid(args[0])
            killed_id = utilities.parse_userid(args[1])
            server_id = ctx.guild.id
            models.leaderboard.add_killed(server_id, killer_id, killed_id)
            await ctx.channel.send("Done")


    @bot.command(
        help="¿leaderboard show the top 5 teamkillers",
        brief="¿leaderboard show the top 5 teamkillers"
    )
    async def leaderboard(ctx):
        leaderboard_doc = models.leaderboard.get_leaderboard(ctx.guild.id)

        for killer in leaderboard_doc:
            killer_name = await get_discord_username(ctx, killer["killer_id"])
            embed = discord.Embed(title=killer_name, color=0x03f8fc)

            for user in killer["killed"]:
                member_name = await get_discord_username(ctx, user)
                embed.add_field(name=member_name, value=killer["killed"][user])

            embed.add_field(name="Total", value=killer["total"])
            await ctx.channel.send(embed=embed)


    @bot.command(
        help="¿find @user get the teamkill stats of a specific user",
        brief="¿find @user get the teamkill stats of a specific user"
    )
    async def find(ctx, *args):

        if len(args) > 1 or len(args) == 0 or args[0] == "@everyone":
            await ctx.channel.send("error")

        else:
            killer_id = utilities.parse_userid(args[0])
            killer_name = await get_discord_username(ctx, killer_id)

            embed = discord.Embed(title=killer_name, color=0x03f8fc)

            killer = models.leaderboard.get_killer(ctx.guild.id, killer_id)

            for user in killer["killed"]:
                member_name = await get_discord_username(ctx, user)
                embed.add_field(name=member_name, value=killer["killed"][user])

            embed.add_field(name="Total", value=killer["total"])
            await ctx.channel.send(embed=embed)


    @bot.event
    async def on_ready():
        print('Online')

    bot.run(TOKEN)
