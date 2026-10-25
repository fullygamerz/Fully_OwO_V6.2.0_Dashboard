"""
This code is only made for educational and practice purposes. 
Author and Fully Development are not responsible for misuse.

Fully OwO V4 Alpha Build
Stable Alpha Build Version: 110126.4.0.3

GitHub: https://github.com/fullygamerz
Discord: https://discord.com/user/fullyneverdies/
"""

import random as fullygamerz_random
import time
import re
import unicodedata
import asyncio as fullygamerz_async
from datetime import datetime, timedelta
from .utils import fullygamerz
from .modules import parse_zoo_message, fetch_zoo_data, format_value, parse_gems, SPEED_MODES
from .fullygamerzcorehb import fullySolveNormalCap, fullySyncedCaptchaSolve
from .state import write_state as _write_state, add_log as _add_log

fullygamerz_start_time = datetime.now()
fullygamerz_commands_sent = 0
fullygamerz_gems_used = 0
last_gem_check = 0

running = True
pray_loop_running = True
has_started = False
sleep_mode = False
farming_start_time = None 
sleep_start_time = None

current_speed_mode = "durable"  
last_mode_change_time = datetime.now()
lifetime_work_cycles = 0  
lifetime_day_skip_active = False 
lifetime_cycle_start_time = None

initial_cash = 0
initial_essence = 0
current_cash = 0
current_essence = 0
zoo_channel = None

fullyHbAlrActiveVar = False
fullyHuntbotTimestampJson = "fullygamerzhbtps.json"

fullyCoreAvailCheck = True

def _push_state():
    """Write current bot state to state.json for the dashboard."""
    _write_state(
        running=running,
        has_started=has_started,
        sleep_mode=sleep_mode,
        speed_mode=current_speed_mode,
        commands_sent=fullygamerz_commands_sent,
        gems_used=fullygamerz_gems_used,
        hb_active=fullyHbAlrActiveVar,
        lifetime_cycles=lifetime_work_cycles,
        lifetime_day_skip=lifetime_day_skip_active,
        start_time=fullygamerz_start_time,
        captcha_solver_ok=fullyCoreAvailCheck,
    )


def ParsefullyTimeStrs(time_str):
    time_str = time_str.upper().strip()
    h = int(re.search(r'(\d+)H', time_str).group(1)) if 'H' in time_str else 0
    m = int(re.search(r'(\d+)M', time_str).group(1)) if 'M' in time_str else 0
    return timedelta(hours=h, minutes=m)

def LoadfullysHbData():
    try:
        import json as fullyop
        import os as fullygamerz_os
        if fullygamerz_os.path.exists(fullyHuntbotTimestampJson):
            with open(fullyHuntbotTimestampJson, "r") as f:
                return fullyop.load(f)
    except: pass
    return {}

def SaveHbDatafullys(data):
    import json as fullyop
    with open(fullyHuntbotTimestampJson, "w") as f:
        fullyop.dump(data, f, indent=4)

def fullyEmbedParser(msg_content):
    try:
        content = msg_content.lower().replace(",", "")
        match = re.search(r"current max autohunt:.*?for (\d+) cowoncy", content)
        if match:
            return int(match.group(1))
    except: pass
    return 20000 

async def fullyCapUrlSolver(url):
    try:
        if fullySolveNormalCap:
            try: return await fullySolveNormalCap(url)
            except: pass
        if fullySyncedCaptchaSolve:
            try: return fullySyncedCaptchaSolve(url)
            except: pass
    except: pass
    return None

async def CheckfullyHbMsgFetch(ctx, cowoncy_amount=None):
    global fullyHbAlrActiveVar
    try:
        await fullygamerz_async.sleep(1)
        messages = await ctx.channel.history(limit=5).flatten()

        for msg in messages:
            if msg.author.id != 408785106942164992:
                continue

            msg_content = str(msg.content)
            if not msg_content and msg.embeds:
                embed = msg.embeds[0]
                msg_content = (embed.description or "") + "".join(f"{f.name}\n{f.value}" for f in embed.fields)
            msg_content_lower = msg_content.lower()

            if "beep. boop. i am huntbot" in msg_content_lower:
                optimal_cowoncy = fullyEmbedParser(msg_content)
                print(f"HuntBot: Found optimal cowoncy: {optimal_cowoncy}")
                
                data = LoadfullysHbData()
                data["optimal_cowoncy"] = optimal_cowoncy
                data["channel_id"] = ctx.channel.id
                SaveHbDatafullys(data)
                
                await fullygamerz_async.sleep(2)
                await ctx.send(f"owo hb {optimal_cowoncy}")
                await fullygamerz_async.sleep(4)
                return await CheckfullyHbMsgFetch(ctx, optimal_cowoncy)

            if "i will be back in" in msg_content_lower:
                match = re.search(r"i will be back in (\d+h\s*\d*m?|\d+m)", msg_content_lower)
                if match:
                    time_str = match.group(1).strip()
                    delta = ParsefullyTimeStrs(time_str)
                    next_time = datetime.now() + delta
                    
                    data = LoadfullysHbData()
                    data.update({
                        "next_huntbot_time": next_time.isoformat(),
                        "is_hunting": True,
                        "last_updated": datetime.now().isoformat(),
                        "channel_id": ctx.channel.id
                    })
                    SaveHbDatafullys(data)
                    
                    fullyHbAlrActiveVar = True
                    print(f"⏰ Next huntbot in {delta} (at {next_time.strftime('%H:%M:%S')})")
                    await ctx.send(f" ⏰ HuntBot will trigger in {delta}")
                    return True

            if "here is your password!" in msg_content_lower and msg.attachments:
                url = msg.attachments[0].url
                print(f"🔍 Solving captcha from {url}")
                result = await fullyCapUrlSolver(url)

                if result:
                    use_cowoncy = cowoncy_amount or LoadfullysHbData().get("optimal_cowoncy", 20000)
                    await fullygamerz_async.sleep(2)
                    await ctx.send(f"owo autohunt {use_cowoncy} {result}")
                    print(f"✅ Auto-solved HuntBot: `{result}` (Used {use_cowoncy})")
                    
                    await fullygamerz_async.sleep(4)
                    return await CheckfullyHbMsgFetch(ctx, use_cowoncy)
                else:
                    await ctx.send(" ❌ Fully Core Module failed to solve HuntBot. Please join the support server to get help.")
                    return False

            if ("you spent" in msg_content_lower and "cowoncy" in msg_content_lower and 
                "i will be back in" in msg_content_lower):
                match = re.search(r"i will be back in (\d+h\s*\d*m?|\d+m)", msg_content_lower)
                if match:
                    time_str = match.group(1).strip()
                    delta = ParsefullyTimeStrs(time_str)
                    next_time = datetime.now() + delta
                    
                    data = LoadfullysHbData()
                    data.update({
                        "next_huntbot_time": next_time.isoformat(),
                        "is_hunting": True,
                        "last_updated": datetime.now().isoformat(),
                        "channel_id": ctx.channel.id,
                        "hunt_stage": "waiting_for_return" 
                    })
                    SaveHbDatafullys(data)
                    
                    fullyHbAlrActiveVar = True
                    print(f"🎯 Hunt started Will return in {delta} (at {next_time.strftime('%H:%M:%S')})")
                    await ctx.send(f"🎯 Hunt active Bot will return in {delta}")
                    return True

            if "i am back with" in msg_content_lower and "animals" in msg_content_lower:
                print(f"🎉 Hunt completed! Bot is back with animals")
                await ctx.send("🎉 Hunt completed! Restarting HuntBot in 15 seconds")
                await fullygamerz_async.sleep(15)
                
                await ctx.send("owo hb")
                print(f"📤 Sent: owo hb (after hunt return)")
                await fullygamerz_async.sleep(4)
                return await CheckfullyHbMsgFetch(ctx)

        return False
    except Exception as e:
        print(f"⚠️ Error in CheckfullyHbMsgFetch: {e}")
        return False

@fullygamerz.command(aliases=["h"])
async def help(ctx):
    fullygamerz_help = """
    # 🤑 Fully OwO Farm V6.0.2 🤑 
Prefix: `.`

**__Main__**
 🌟 Start: *Starts The AutoBot*
 🛑 Stop: *Stops The AutoBot*
 🔍 Status: *Shows Bot Status*
 ⚡ Speed: *Change speed mode (efficient/fast/durable/lifetime)*

**__Features__**
 ⚠ Ban Bypass
 🚨 Auto Detects OwO Warnings
 ⏱ Auto Cut After 1 Warning
 💎 Auto Use Gems 
 🦁 Zoo Value Tracking & Profit Calculator
 🏹 Fast And Secure
 🛏️ Smart Dynamic Auto Sleep
 🎯 Auto HuntBot Integration with Auto Solver
 ♾️ Lifetime Mode with Advanced Detection Protection

**__Made with 💖 and 🧠 by Fully | [Fully Development]__** 
"""
    await ctx.send(fullygamerz_help)  

@fullygamerz.command()
async def speed(ctx, mode: str = None):
    global current_speed_mode, last_mode_change_time
    
    if mode is None:
        current_config = SPEED_MODES[current_speed_mode]
        await ctx.send(f"Current speed mode: **{current_config['name']}**\n\nAvailable modes: `efficient`, `fast (Not Recommended)`, `durable (Recommended)`, `lifetime (Bypass Detection)`")
        return
    
    mode = mode.lower()
    
    if mode not in SPEED_MODES:
        await ctx.send("❌ Invalid speed mode. Available modes: `efficient`, `fast (Not Recommended)`, `durable (Recommended)`, `lifetime (Bypass Detection)`")
        return
    
    current_speed_mode = mode
    last_mode_change_time = datetime.now()
    current_config = SPEED_MODES[current_speed_mode]
    
    await ctx.send(f"✅ Speed mode changed to: **{current_config['name']}**")

async def do_gem_check(ctx):
    global fullygamerz_gems_used 
    if sleep_mode:
        return
    
    await ctx.send("owo inventory")
    
    current_config = SPEED_MODES[current_speed_mode]
    await fullygamerz_async.sleep(3)  
    
    try:
        latest_messages = await ctx.channel.history(limit=2).flatten()
        
        for message in latest_messages:
            if message.author.id == 408785106942164992:  
                if "inventory" in message.content.lower():
                    gem_numbers = await parse_gems(message.content)
                    if gem_numbers: 
                        use_command = "owo use " + " ".join(gem_numbers)
                        await ctx.send("owo lb all")
                        await ctx.send(use_command)
                        fullygamerz_gems_used += len(gem_numbers)
                        await fullygamerz_async.sleep(3)
                    else:
                        print("No gems found")
                    break
    except Exception as e:
        print(f"Error in gem check: {e}")
        import traceback
        print(traceback.format_exc())

async def check_warning(ctx):
    global running
    if sleep_mode:
        return False

    try:
        messages = await ctx.channel.history(limit=10).flatten()

        for msg in messages:

            msg_content = str(msg.content)
            if not msg_content:
                continue
            msg_content_clean = unicodedata.normalize("NFKC", msg_content)
            msg_content_clean = re.sub(r'[\u200B-\u200D\uFEFF]', '', msg_content_clean)
            msg_content_lower = msg_content_clean.lower()

            if "captcha" in msg_content_lower and "verify" in msg_content_lower:
                warning_pattern = r'[\(\[\{]?\s*(\d+)\s*[\/／]\s*5\s*[\)\]\}]?'
                match = re.search(warning_pattern, msg_content_lower)

                if match:
                    warning_count = int(match.group(1))
                    print(f"⚠️ CAPTCHA WARNING DETECTED: ({warning_count}/5)")

                    if warning_count == 1:
                        running = False
                        _add_log("⚠️", f"CAPTCHA WARNING (1/5) — bot stopped! Solve manually.", "warn")
                        _push_state()
                        await ctx.send(
                            "⚠ WARNING DETECTED! 🛑 Stopping | **SOLVE YOUR CAPTCHA FIRST** | "
                            "Then Type `.start` again to restart grinding."
                        )
                        print("⚠ Stopped due to CAPTCHA (1/5)")
                        return True

        return False

    except Exception as e:
        print(f"Warning check error: {e}")
        return False


async def monitor_huntbot(ctx):
    global fullyHbAlrActiveVar
    
    while running:
        try:
            data = LoadfullysHbData()
            if "next_huntbot_time" in data and data.get("channel_id") == ctx.channel.id:
                next_time_str = data["next_huntbot_time"]
                next_time = datetime.fromisoformat(next_time_str)
                current_time = datetime.now()

                if current_time >= next_time and data.get("is_hunting"):
                    print(f"⏰ HuntBot timer reached! Triggering HuntBot...")
                    await ctx.send("⏰ HuntBot timer reached! Restarting...")
                    data["is_hunting"] = False
                    SaveHbDatafullys(data)
                    fullyHbAlrActiveVar = False
                    await fullygamerz_async.sleep(2)
                    await ctx.send("owo hb")
                    print(f"📤 Sent: owo hb (auto-triggered by timer)")
                    await fullygamerz_async.sleep(4)
                    await CheckfullyHbMsgFetch(ctx)

            await fullygamerz_async.sleep(30)
            
        except Exception as e:
            print(f"⚠️ Error in monitor_huntbot: {e}")
            await fullygamerz_async.sleep(60)


@fullygamerz.command()
async def start(ctx):
    global running, last_gem_check, fullygamerz_commands_sent, has_started
    global initial_cash, initial_essence, zoo_channel, sleep_mode, sleep_start_time
    global last_mode_change_time, fullygamerz_start_time, farming_start_time
    global lifetime_work_cycles, lifetime_day_skip_active, lifetime_cycle_start_time
    
    if running and has_started:
        await ctx.send("⚠️ **Fully OwO Worker is already running!**\n\n🛑 Please use `.stop` first, then `.start` to restart/force fix the worker.\nJoin the support server for better guidance.")
        return
    
    running = True
    sleep_mode = False
    has_started = True
    zoo_channel = ctx.channel
    last_gem_check = time.time()
    last_command = None
    sleep_start_time = None
    farming_start_time = datetime.now()
    last_mode_change_time = datetime.now()
    _add_log("🟢", f"Bot started — speed: {current_speed_mode}", "hunt")
    _push_state()
    
    lifetime_work_cycles = 0
    lifetime_day_skip_active = False
    lifetime_cycle_start_time = datetime.now()
    
    current_config = SPEED_MODES[current_speed_mode]
    zoo_data = await fetch_zoo_data(ctx)
    
    if zoo_data:
        initial_cash = zoo_data['total_cash']
        initial_essence = zoo_data['total_essence']

    await fullygamerz_async.sleep(2)
    data = LoadfullysHbData()
    data["channel_id"] = ctx.channel.id
    SaveHbDatafullys(data)
    await ctx.send("owo hb")
    await fullygamerz_async.sleep(4)
    await CheckfullyHbMsgFetch(ctx)
    
    fullygamerz.loop.create_task(monitor_huntbot(ctx))
    fullygamerz.loop.create_task(_state_writer_loop())
    
    await fullygamerz_async.sleep(2)

    while running:
        try:
            
            if has_started and running and not sleep_mode:
                current_time = datetime.now()
                if current_speed_mode == "lifetime":
                    current_config = SPEED_MODES["lifetime"] 
                    if not lifetime_day_skip_active:
                        should_skip_day = fullygamerz_random.random() < 0.5  
                        if lifetime_work_cycles >= fullygamerz_random.randint(3, 4) and should_skip_day:
                            lifetime_day_skip_active = True
                            day_skip_duration = 24 * 3600 
                            skip_end_time = current_time + timedelta(seconds=day_skip_duration)
                            
                            await ctx.send(f"😴 **LIFETIME MODE: DAY SKIP ACTIVATED** 🌙\nFull 24-hour rest. Will resume at **{skip_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}**")
                            print(f"⏸️ LIFETIME DAY SKIP: Will resume at {skip_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}")
                            
                            await fullygamerz_async.sleep(day_skip_duration)
                            
                            lifetime_day_skip_active = False
                            lifetime_work_cycles = 0  
                            farming_start_time = datetime.now()
                            lifetime_cycle_start_time = datetime.now()
                            await ctx.send("⏰ **LIFETIME MODE: RESUMING AFTER DAY SKIP** 🚀")
                            print("⏰ LIFETIME DAY SKIP ENDED: Resuming")
                            continue
                    
                    if lifetime_cycle_start_time is None:
                        lifetime_cycle_start_time = current_time
                    
                    work_duration = fullygamerz_random.uniform(
                        current_config['work_duration_min'],
                        current_config['work_duration_max']
                    )
                    
                    elapsed_cycle_time = (current_time - lifetime_cycle_start_time).total_seconds()
                    
                    if elapsed_cycle_time >= work_duration:
                        sleep_mode = True
                        break_duration = fullygamerz_random.uniform(
                            current_config['break_duration_min'],
                            current_config['break_duration_max']
                        )
                        sleep_start_time = current_time
                        sleep_end_time = current_time + timedelta(seconds=break_duration)
                        
                        lifetime_work_cycles += 1
                        hours, remainder = divmod(int(break_duration), 3600)
                        mins = remainder // 60
                        
                        await ctx.send(f"😴 **LIFETIME MODE: BREAK TIME** 🌙\nWork cycle #{lifetime_work_cycles} complete. Breaking for {hours}h {mins}m. Resume at **{sleep_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}**")
                        print(f"😴 LIFETIME BREAK: Cycle #{lifetime_work_cycles} done. Breaking for {hours}h {mins}m")
                        
                        await fullygamerz_async.sleep(break_duration)
                        
                        sleep_mode = False
                        lifetime_cycle_start_time = datetime.now()
                        await ctx.send(f"⏰ **LIFETIME MODE: BACK TO WORK** 🚀\nStarting work cycle #{lifetime_work_cycles + 1}")
                        print(f"⏰ LIFETIME WORK CYCLE: Resuming cycle #{lifetime_work_cycles + 1}")
                        continue
                
                else:
                    active_mode = current_speed_mode
                    max_run_time = (current_time - last_mode_change_time).total_seconds()
                    
                    current_config = SPEED_MODES[active_mode]
                    elapsed_time = (current_time - farming_start_time).total_seconds()
                    
                    max_run_time = fullygamerz_random.uniform(
                        current_config['run_duration_min'],
                        current_config['run_duration_max']
                    )
                    
                    if elapsed_time >= max_run_time:
                        sleep_mode = True
                        sleep_duration = fullygamerz_random.uniform(
                            current_config['sleep_duration_min'],
                            current_config['sleep_duration_max']
                        )
                        sleep_start_time = current_time
                        sleep_end_time = current_time + timedelta(seconds=sleep_duration)
                        
                        await ctx.send(f"😴 Entering sleep mode. Will resume at **{sleep_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}**")
                        print(f"Sleep mode started. Will resume at {sleep_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}")
                        _add_log("😴", f"Sleep mode — resumes at {sleep_end_time.strftime('%H:%M:%S')}", "sleep")
                        _push_state()
                        
                        await fullygamerz_async.sleep(sleep_duration)
                        
                        sleep_mode = False
                        farming_start_time = datetime.now()
                        last_mode_change_time = datetime.now()
                        await ctx.send("⏰ Waking up from sleep. Resuming")
                        print("⏰ Waking up from sleep. Resuming")
                        _add_log("⏰", "Woke up — resuming grind 🚀", "hunt")
                        _push_state()
                        continue

            if sleep_mode:
                await fullygamerz_async.sleep(10)
                continue

            current_time = time.time()
            current_config = SPEED_MODES[current_speed_mode]
            
            gem_check_interval = fullygamerz_random.randint(
                int(current_config['gem_check_interval_min']), 
                int(current_config['gem_check_interval_max'])
            )
            
            if current_time - last_gem_check >= gem_check_interval:
                warning_detected = await check_warning(ctx)
                if warning_detected or not running:
                    break
                await do_gem_check(ctx)
                last_gem_check = current_time
                continue

            def fullygamerzsmarttypo(command):
                if fullygamerz_random.random() < 0.12:
                    idx = fullygamerz_random.randint(0, len(command)-1)
                    fullygamerztypochars = fullygamerz_random.choice('abcdefghijklmnopqrstuvwxyz')
                    return command[:idx] + fullygamerztypochars + command[idx+1:]
                return command

            commands = [
                fullygamerzsmarttypo("owoh"), fullygamerzsmarttypo("owo pray"), fullygamerzsmarttypo("owo h"), fullygamerzsmarttypo("owo b"), fullygamerzsmarttypo("owob"),
                fullygamerzsmarttypo("owoh"), fullygamerzsmarttypo("owo h"),
                fullygamerzsmarttypo(fullygamerz_random.choice(["owo cf 1", "owoz", "owo s 2", "owo owo", "owoq"])),
                fullygamerzsmarttypo(fullygamerz_random.choice(["owo pup", "owo army", "owo piku", "owo run"])),
                fullygamerzsmarttypo(fullygamerz_random.choice(["owo punch <@408785106942164992>", "owo roll"]))
            ]
            command = fullygamerz_random.choice(commands)

            while command == last_command:
                command = fullygamerz_random.choice(commands)
            last_command = command

            await ctx.send(command)
            fullygamerz_commands_sent += 1
            _push_state()
            _add_log("📤", f"Sent: {command}", "cmd")

            await fullygamerz_async.sleep(current_config['command_delay'])
            warning_detected = await check_warning(ctx)
            if warning_detected or not running:
                break

            await fullygamerz_async.sleep(fullygamerz_random.uniform(
                current_config['action_delay_min'], 
                current_config['action_delay_max']
            ))
            if fullygamerz_random.random() < 0.05:
                await fullygamerz_async.sleep(fullygamerz_random.uniform(
                    current_config['random_long_delay_min'], 
                    current_config['random_long_delay_max']
                ))

        except Exception as e:
            print(f"Error in main loop: {e}")


@fullygamerz.command()  
async def stop(ctx):
    global running, has_started, sleep_mode
    await ctx.send(
        "🛑 Stopping | Type .start again to re-start grinding"
    )  
    running = False
    has_started = False
    sleep_mode = False
    _add_log("🛑", "Bot stopped by user", "warn")
    _push_state()


@fullygamerz.command()
async def status(ctx):
    global fullygamerz_start_time, fullygamerz_commands_sent, fullygamerz_gems_used, last_gem_check, has_started
    global initial_cash, initial_essence, current_cash, current_essence, zoo_channel, current_speed_mode
    global sleep_mode, sleep_start_time, lifetime_work_cycles, lifetime_day_skip_active, lifetime_cycle_start_time
    
    current_config = SPEED_MODES[current_speed_mode]
    
    if current_speed_mode == "lifetime":
        if lifetime_day_skip_active:
            fullygamerz_state = f"🌙 Day Skip Mode ({current_config['name']})"
        elif sleep_mode:
            fullygamerz_state = f"😴 Break Time (Cycle #{lifetime_work_cycles}) ({current_config['name']})"
        elif has_started and running:
            fullygamerz_state = f"🚀 Working (Cycle #{lifetime_work_cycles + 1}) ({current_config['name']})"
        else:
            fullygamerz_state = f"⚫ Not Running ({current_config['name']})"
    else:
        if sleep_mode:
            fullygamerz_state = f"😴 Sleeping ({current_config['name']})"
            if sleep_start_time:
                sleep_elapsed = datetime.now() - sleep_start_time
                hrs, rem = divmod(int(sleep_elapsed.total_seconds()), 3600)
                mins, secs = divmod(rem, 60)
                fullygamerz_state += f" | Slept: {hrs}h {mins}m {secs}s"
        elif has_started and running:
            fullygamerz_state = f"🟢 Running ({current_config['name']})"
        else:
            fullygamerz_state = f"⚫ Not Running ({current_config['name']})"
    
    fullygamerz_uptime = datetime.now() - fullygamerz_start_time
    hrs, rem = divmod(int(fullygamerz_uptime.total_seconds()), 3600)
    mins, secs = divmod(rem, 60)

    profit_text = ""
    if has_started and zoo_channel and not sleep_mode:
        await ctx.send("🔍 Fetching current zoo data for profit calculation...")
        
        await zoo_channel.send("owo zoo")
        await fullygamerz_async.sleep(3)
        
        try:
            messages = await zoo_channel.history(limit=10).flatten()
            zoo_messages = []
            
            for msg in messages:
                if msg.author.id == 408785106942164992:
                    if any(keyword in msg.content.lower() for keyword in ['zoo', 'animals', 'cowoncy']):
                        zoo_messages.append(msg.content)
            
            if zoo_messages:
                zoo_data = await parse_zoo_message(zoo_messages)
                current_cash = zoo_data['total_cash']
                current_essence = zoo_data['total_essence']
                
                cash_profit = current_cash - initial_cash
                essence_profit = current_essence - initial_essence
                
                profit_text = f"\n\n💰 **Profit Since Start:**\n> 💵 Cash: {format_value(cash_profit)} ({format_value(initial_cash)} → {format_value(current_cash)})\n> ✨ Essence: {format_value(essence_profit)} ({format_value(initial_essence)} → {format_value(current_essence)})"
        except Exception as e:
            print(f"Error fetching status zoo data: {e}\n\nJoin the support server for help.")
            profit_text = "\n\n⚠ Could not fetch current zoo data\nJoin the support server for help."

    lifetime_info = ""
    if current_speed_mode == "lifetime":
        lifetime_info = f"\n> ♾️ **Work Cycles:** {lifetime_work_cycles}\n> 🌙 **Day Skip Active:** {'Yes' if lifetime_day_skip_active else 'No'}"
        if lifetime_cycle_start_time:
            cycle_elapsed = datetime.now() - lifetime_cycle_start_time
            cycle_hrs, cycle_rem = divmod(int(cycle_elapsed.total_seconds()), 3600)
            cycle_mins = cycle_rem // 60
            lifetime_info += f"\n> ⏱️ **Current Cycle Duration:** {cycle_hrs}h {cycle_mins}m"

    gstatusfullygamerz = f"""
🔍 **fully OwO Status:** {fullygamerz_state}

> 🕒 **Running Since:** {fullygamerz_start_time.strftime('%d-%b-%Y %I:%M:%S %p')}
> 📈 **Uptime:** {hrs}h {mins}m {secs}s
> 📊 **Commands Sent:** {fullygamerz_commands_sent}
> 💎 **Gems Potentially Used:** {fullygamerz_gems_used}
> ⚡ **Speed Mode:** {current_config['name']}{lifetime_info}
> 🛏️ **Sleeping?:** {"Yes" if sleep_mode else "No"}
> 🎯 **HuntBot Active?:** {"Yes" if fullyHbAlrActiveVar else "No"}
> 🧠 **HuntBot Solver:** {"Available" if fullyCoreAvailCheck else "Not Available"}
> ♻️ **Last Gem Check:** {'<t:' + str(int(last_gem_check)) + ':R>' if last_gem_check else 'Never'}{profit_text}
"""
    await ctx.send(gstatusfullygamerz)


async def _state_writer_loop():
    """Write state every second so dashboard stays up to date."""
    while True:
        try:
            _push_state()
        except:
            pass
        import asyncio as _a
        await _a.sleep(1)
