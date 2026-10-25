"""
This code is only made for educational and practice purposes. 
Author and Fully Development are not responsible for misuse.

Fully OwO V4 Alpha Build
Stable Alpha Build Version: 110126.4.0.3

GitHub: https://github.com/fullygamerz
Discord: https://discord.com/user/fullyneverdies/
"""

import discord
from discord.ext import commands
from colorama import Fore, Style

fullygamerzop = discord.Intents.all()
fullyyy = "."
fullygamerz = commands.Bot(
    command_prefix=fullyyy, case_insensitive=True, self_bot=True, intents=fullygamerzop
)
fullygamerz.remove_command("help")

@fullygamerz.event
async def on_ready():
    print(
        f"{Fore.LIGHTRED_EX} > Fully OwO Farm v6 Alpha Connected To:{Style.RESET_ALL}",
        f"{Fore.LIGHTGREEN_EX}{fullygamerz.user}{Style.BRIGHT}{Style.RESET_ALL}",
    )
    print(f"{Fore.LIGHTRED_EX} > Added Lifetime Mode{Style.RESET_ALL}")
    print(f"{Fore.LIGHTRED_EX} > Updated - 11 January 2026 [Join Fully Development For Further Updates]{Style.RESET_ALL}")
