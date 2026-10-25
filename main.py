"""
This code is only made for educational and practice purposes. 
Author and Fully Development are not responsible for misuse.

Fully OwO V4 Alpha Build
Stable Alpha Build Version: 110126.4.0.3

GitHub: https://github.com/fullygamerz
Discord: https://discord.com/user/fullyneverdies/
"""

import os as fullygamerz_os

fullygamerz_os.system("pip install -r requirements.txt")
fullygamerz_os.system(
    "sleep 2 && clear >/dev/null 2>&1 &"
    if fullygamerz_os.name == "posix"
    else "timeout /t 2 >nul 2>&1 && cls"
)

import json as fullyop
from colorama import Fore, Style, init
from core.utils import fullygamerz
from core.heart import fullygamerz_start_time, fullygamerz_commands_sent, fullygamerz_gems_used, running

print(
    f"""{Fore.BLUE}
           ▒▒                    ▒▒            ▒▒       ▒▒▒      ░░░░░░
        ▒▒▒▒▒▒▒   ▒▒▒     ▒▒▒▒ ▒▒▒▒▒▒▒▒        ▒▒▒▒     ▒▒▒▒    ░░░░██░░
      ▒▒▒▒████▒▒ ▒▒█▒▒  ▒▒▒█▒▒▒▒░█████▒        ▒█▒▒   ▒▒▒██▒   ░░████░░░░
     ▒▒▒▒██░░██▒▒▒██▒▒ ▒▒░██▒░▒██░░░░█▒        ▒██▒▒ ▒▒██░▒▒  ░░██░░░░░░░
     ▒▒██░░░░██▒▒██▒▒▒ ▒░██▒▒██░░░░░░█▒        ▒▒█▒▒▒▒██▒▒▒   ░░█░░░░░░░░░
    ▒▒██░░█░░█▒▒▒█▒▒▒▒▒▒░█▒▒▒█░░░█░░██▒         ▒█▒▒▒██▒▒    ░░██░██████░░░
    ▒▒█░░░░░░█▒▒█░░██░▒░█▒▒ ▒█░░░░░█▒▒▒         ▒░█▒██▒▒     ░░███░░░░░██░░░
    ▒▒█░░░░██▒▒▒████████▒▒  ▒██░░███▒▒          ▒▒██░▒       ░░░██░░░░░░██░
     ▒██████▒▒▒███▒▒▒██▒▒   ▒▒████▒▒▒            ▒█▒▒         ░░░██░░░░██░░
    ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒     ▒▒▒▒▒▒              ▒▒▒          ░░░░░████░░░
     ▒▒▒▒▒    ▒▒▒▒▒▒▒▒▒      ▒▒▒▒▒               ▒▒▒            ░░░░░░░░
               ▒▒   ▒▒        ▒▒                 ▒▒              ░░░░░░
               
               
                                                 Fully Development Alpha Build Version: 110126.4.0.3{Style.RESET_ALL}"""
)

init(autoreset=True)
print(f"{Fore.LIGHTRED_EX}\n\n > Made By Fully [Fully Development]{Style.RESET_ALL}")

with open("config.json", "r") as config_file:
    config = fullyop.load(config_file)

fullygamerzopaf = config["TOKEN"]  
fullygamerz.run(fullygamerzopaf, bot=False)
