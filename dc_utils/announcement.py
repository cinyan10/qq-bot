# This example requires the 'message_content' privileged intent to function.
from __future__ import annotations

import datetime
import os
from discord import Embed
from discord.ext import commands
import discord
import dotenv


ANNOUNCEMENTS = [
    Embed(title="👋 **Welcome to the AXE Kreedz Community!** 🎉",
          description="""
                  
                    We're thrilled to have you join our server. Whether you're a seasoned Kreedz player or new to the scene, you've come to the right place for a fun and challenging experience.
                    
                    Here's a few things to get you started:
                    
                    🎮 Server IP: <#1078216816482062367>
                    🏆 Check out our Kreedz maps in the server and start your climbing journey.
                    💬 Feel free to chat and interact with our friendly community members.
                    ❓ If you have any questions or need assistance, don't hesitate to ask in the <#1198635192496173227>  channel.
                    📅 Keep an eye out for server events and tournaments. It's a great way to showcase your skills and win cool prizes!
                    
                    Remember to follow the server rules and respect your fellow players. Let's make this community a welcoming and enjoyable place for everyone.
                    
                    Enjoy your time here, and happy climbing! 🧗‍♂️
                    
                  """,
          color=discord.Color.blue(),
          timestamp=datetime.datetime.now()
          ),
    Embed(title="👋 **欢迎来到 AXE Kreedz 社区！** 🎉",
          description="""
                  
                    我们非常高兴您加入我们的服务器。无论您是经验丰富的 Kreedz 玩家还是新手，您都来对地方了，这里提供了一个有趣而具有挑战性的体验。
                    
                    以下是一些入门信息：
                    
                    🎮 服务器IP：<#1078216816482062367>
                    🏆 在服务器中查看我们的 Kreedz 地图，并开始您的攀爬之旅。
                    💬 随时与我们友好的社区成员聊天和互动。
                    ❓ 如果您有任何问题或需要帮助，请在 <#1198635192496173227> 频道中提问，不要犹豫。
                    📅 请关注服务器活动和比赛。这是展示您技能并赢得酷炫奖品的好机会！
                    
                    请记住遵守服务器规则并尊重其他玩家。让我们一起把这个社区打造成一个对每个人都友好和愉快的地方。
                    
                    享受您在这里的时光，快乐攀爬！ 🧗‍♂️
                    
                  """"",
          color=discord.Color.blue(),
          timestamp=datetime.datetime.now()
          ),
    Embed(title="👋 **歡迎來到 AXE Kreedz 社群！** 🎉",
          description="""
                  
                    我們非常高興您加入我們的伺服器。無論您是經驗豐富的 Kreedz 玩家還是新手，您都來對地方，這裡提供了一個有趣而具有挑戰性的體驗。
                    
                    以下是一些入門信息：
                    
                    🎮 伺服器IP：<#1078216816482062367>
                    🏆 在伺服器中查看我們的 Kreedz 地圖，並開始您的攀爬之旅。
                    💬 隨時與我們友好的社群成員聊天和互動。
                    ❓ 如果您有任何問題或需要幫助，請在 <#1198635192496173227> 頻道中提問，不要猶豫。
                    📅 請關注伺服器活動和比賽。這是展示您技能並贏得酷炫獎品的好機會！
                    
                    請記住遵守伺服器規則並尊重其他玩家。讓我們一起把這個社群打造成一個對每個人都友好和愉快的地方。
                    
                    享受您在這裡的時光，快樂攀爬！ 🧗‍♂️
                    
                  """,
          color=discord.Color.blue(),
          timestamp=datetime.datetime.now()
          )
]


# Define a simple View that persists between bot restarts
# In order for a view to persist between restarts it needs to meet the following conditions:
# 1) The timeout of the View has to be set to None
# 2) Every item in the View has to have a custom_id set
# It is recommended that the custom_id be sufficiently unique to
# prevent conflicts with other buttons the bot sends.
# For this example the custom_id is prefixed with the name of the bot.
# Note that custom_ids can only be up to 100 characters long.
class AnnouncementView(discord.ui.View):
    def __init__(self):  # NOQA
        super().__init__(timeout=None)
        self.embeds = ANNOUNCEMENTS
        if not hasattr(self, 'fields_added'):
            self.fields_added = True
            self.embeds[0].add_field(name="**HOW TO GET WHITELISTED:**", value="""
**Requirements:**

- Achieve 50,000 points in any game mode.
- Must not be banned by VAC (Valve Anti-Cheat).
- Must not be banned from multiple games.

**Join Our Steam Group:**

- Ensure that your Steam profile is set to public (to verify your membership in our Steam group).

**Request Whitelisting:**

- Use the command `/bind_steam` in the <#1192079597399965847> to bind your Steam ID.
- After binding your Steam ID, use the command `/whitelist` to request whitelisting.
         """, inline=False)

            self.embeds[1].add_field(name="**如何获得白名单:**", value="""
**要求:**

- 在任意游戏模式中达到 50,000 分。
- 不能被 VAC (Valve 反作弊系统) 封禁。
- 不能在多个游戏中被封禁。

**加入我们的 Steam 群组:**

- 确保您的 Steam 档案设置为公开（以验证您是否加入了我们的 Steam 群组）。

**请求白名单:**

- 在 <#1192079597399965847> 频道中使用 `/bind_steam` 命令来绑定您的 Steam ID。
- 绑定您的 Steam ID 后，使用 `/whitelist` 命令来请求白名单。

                    """, inline=False)

            self.embeds[2].add_field(name="**如何獲得白名單:**", value="""
**要求:**

- 在任意遊戲模式中達到 50,000 分。
- 不能被 VAC (Valve 反作弊系統) 封禁。
- 不能在多個遊戲中被封禁。

**加入我們的 Steam 群組:**

- 確保您的 Steam 檔案設置為公開（以驗證您是否加入了我們的 Steam 群組）。

**綁定您的 Steam ID:** 

**請求白名單:**

- 在 <#1192079597399965847> 頻道中使用 `/bind_steam` 命令來綁定您的 Steam ID。
- 綁定您的 Steam ID 後，使用 `/whitelist` 命令來請求白名單。

                            """, inline=False)

        button_web = discord.ui.Button(label="Website", style=discord.ButtonStyle.url,
                                       url="https://www.axekz.com/", emoji="<:axe:1201477183982542888>")
        button_steam = discord.ui.Button(label='Steam Group', style=discord.ButtonStyle.url,
                                         url='https://steamcommunity.com/groups/axekz',
                                         emoji="<:Steam_Logo:1201477320263880796>", row=2)
        button_bili = discord.ui.Button(label='Bilibili', style=discord.ButtonStyle.url,
                                        url="https://space.bilibili.com/1200368090",
                                        emoji="<:bilibili2:1201477844002410566>", row=2)
        button_qq = discord.ui.Button(label='QQ Group', style=discord.ButtonStyle.url,
                                      url='http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=qKG6PDxw4zojM91iS0je7uPvvh7mtOx_'
                                          '&authKey=jeSZf2rXhRy2HR80moAPBkEnqKIN%2FLZRbwM7Nf%2Ft2jUwYmHUXdf6bR49'
                                          '%2F1QDQ3Yf&noverify=0&group_code=188099455',
                                      emoji="<:QQ3:1201477696358719488>", row=2)

        self.add_item(button_web)
        self.add_item(button_bili)
        self.add_item(button_steam)
        self.add_item(button_qq)

    @discord.ui.button(label='English', style=discord.ButtonStyle.grey, custom_id='persistent_view:green', emoji='🇬🇧')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):  # NOQA
        await interaction.response.edit_message(embed=self.embeds[0])  # NOQA

    @discord.ui.button(label='简体中文', style=discord.ButtonStyle.grey, custom_id='persistent_view:red', emoji="🇨🇳")
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):  # NOQA
        await interaction.response.edit_message(embed=self.embeds[1])  # NOQA

    @discord.ui.button(label='繁體中文', style=discord.ButtonStyle.grey, custom_id='persistent_view:grey', emoji='🇹🇼')
    async def grey(self, interaction: discord.Interaction, button: discord.ui.Button):  # NOQA
        await interaction.response.edit_message(embed=self.embeds[2])  # NOQA


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

    # async def setup_hook(self) -> None:
        # self.add_view(AnnouncementView())

        # Register the persistent view for listening here.
        # Note that this does not send the view to any message.
        # In order to do this you need to first send a message with the View, which is shown below.
        # If you have the message_id you can also pass it as a keyword argument, but for this example
        # we don't have one.
        # For dynamic items, we must register the classes instead of the views.
        # self.add_dynamic_items(DynamicButton)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


# @bot.command()
# @commands.is_owner()
# async def prepare(ctx: commands.Context):
#     """Starts a persistent view."""
#     # In order for a persistent view to be listened to, it needs to be sent to an actual message.
#     # Call this method once just to store it somewhere.
#     # In a more complicated program you might fetch the message_id from a database for use later.
#     # However, this is outside the scope of this simple example.
#     await ctx.send("What's your favourite colour?", view=AnnouncementView())


if __name__ == '__main__':
    dotenv.load_dotenv()

    TOKEN = os.getenv('TEST_TOKEN')

    bot = PersistentViewBot()

    bot.run(TOKEN)
