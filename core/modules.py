"""
This code is only made for educational and practice purposes. 
Author and Fully Development are not responsible for misuse.

Fully OwO V4 Alpha Build
Stable Alpha Build Version: 110126.4.0.3

GitHub: https://github.com/fullygamerz
Discord: https://discord.com/user/fullyneverdies/
"""

import re
import asyncio as fullygamerz_async

SPEED_MODES = {
    "efficient": {
        "name": "Efficient (Fast)",
        "command_delay": 0.5,
        "action_delay_min": 5.0,
        "action_delay_max": 15.0,
        "random_long_delay_min": 200,
        "random_long_delay_max": 400,
        "gem_check_interval_min": 200,
        "gem_check_interval_max": 290,
        "run_duration_min": 3 * 3600,  
        "run_duration_max": 3.5 * 3600,  
        "sleep_duration_min": 3.5 * 3600,  
        "sleep_duration_max": 4.5 * 3600   
    },
    "fast": {
        "name": "Fast (Very Fast | Not Recommended, Don't Use)",
        "command_delay": 0.3,
        "action_delay_min": 4.5,
        "action_delay_max": 10.0,
        "random_long_delay_min": 160,
        "random_long_delay_max": 200,
        "gem_check_interval_min": 120,
        "gem_check_interval_max": 180,
        "run_duration_min": 1.5 * 3600,  
        "run_duration_max": 2 * 3600,    
        "sleep_duration_min": 3.5 * 3600,  
        "sleep_duration_max": 5 * 3600     
    },
    "durable": {
        "name": "Durable (Safe & Long)",
        "command_delay": 0.35,
        "action_delay_min": 6.5,
        "action_delay_max": 21.0,
        "random_long_delay_min": 300,
        "random_long_delay_max": 600,
        "gem_check_interval_min": 244,
        "gem_check_interval_max": 415,
        "run_duration_min": 5 * 3600,    
        "run_duration_max": 7 * 3600,    
        "sleep_duration_min": 3.5 * 3600,  
        "sleep_duration_max": 5 * 3600   
    },
    "lifetime": {
        "name": "Lifetime (Ultra Long - Detection Bypass)",
        "command_delay": 0.4,
        "action_delay_min": 7.0,
        "action_delay_max": 22.0,
        "random_long_delay_min": 250,
        "random_long_delay_max": 550,
        "gem_check_interval_min": 220,
        "gem_check_interval_max": 380,
        "work_duration_min": 3 * 3600,  
        "work_duration_max": 5 * 3600,  
        "break_duration_min": 10 * 3600,  
        "break_duration_max": 14 * 3600,  
        "day_skip_threshold": 3, 
        "day_skip_duration": 24 * 3600  
    }
}

def format_value(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return str(value)

async def parse_zoo_message(zoo_messages):
    combined_message = "\n".join(zoo_messages)
    
    
    superscript_map = {
        '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
        '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9'
    }
    
    value_map = {
        "common": {"cash": 1, "essence": 1},
        "uncommon": {"cash": 3, "essence": 5},
        "rare": {"cash": 10, "essence": 20},
        "epic": {"cash": 250, "essence": 250},
        "mythic": {"cash": 5000, "essence": 3000},
        "patreon": {"cash": 1000, "essence": 500},
        "cpatreon": {"cash": 50000, "essence": 25000},
        "legendary": {"cash": 15000, "essence": 10000},
        "gem": {"cash": 30000, "essence": 20000},
        "botrank": {"cash": 50000, "essence": 10000},
        "distorted": {"cash": 300000, "essence": 200000},
        "fabled": {"cash": 250000, "essence": 100000},
        "special": {"cash": 6000, "essence": 5000},
        "hidden": {"cash": 1000000, "essence": 500000}
    }
    
    lines = combined_message.split('\n')
    tier_data = {}
    current_tier = None
    
    for line in lines:
        tier_match = re.search(r'<a?:(\w+):\d+>', line)
        if tier_match:
            tier_name = tier_match.group(1).lower()
            if tier_name in value_map:
                current_tier = tier_name
                tier_data[current_tier] = []
        
        if current_tier:
            animal_regex = r'(<a?:\w+:\d+>|:\w+:)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)'
            for animal_match in re.finditer(animal_regex, line):
                superscript_str = animal_match.group(2)
                number_str = ''.join(superscript_map.get(char, char) for char in superscript_str)
                value = int(number_str) if number_str.isdigit() else 0
                
                if value > 0:
                    for _ in range(value):
                        tier_data[current_tier].append(animal_match.group(1))
    
    total_cash = 0
    total_essence = 0
    
    for tier, animals in tier_data.items():
        if animals and tier in value_map:
            count = len(animals)
            cash_per = value_map[tier]["cash"]
            essence_per = value_map[tier]["essence"]
            total_cash += count * cash_per
            total_essence += count * essence_per
    
    zoo_points = 0
    zoo_points_patterns = [
        r'Zoo Points?:\s*__?([\d,]+)__?',
        r'Points?:\s*__?([\d,]+)__?',
        r'__?([\d,]+)__?\s*Zoo Points?',
    ]
    
    for pattern in zoo_points_patterns:
        match = re.search(pattern, combined_message, re.IGNORECASE)
        if match:
            zoo_points = int(match.group(1).replace(',', ''))
            break
    
    return {
        'total_cash': total_cash,
        'total_essence': total_essence,
        'zoo_points': zoo_points,
        'tier_data': tier_data
    }

async def fetch_zoo_data(ctx):
    """Fetch zoo data by sending owo zoo and parsing response"""
    await ctx.send("owo zoo")
    await fullygamerz_async.sleep(3)
    
    try:
        messages = await ctx.channel.history(limit=10).flatten()
        zoo_messages = []
        
        for msg in messages:
            if msg.author.id == 408785106942164992:
                if any(keyword in msg.content.lower() for keyword in ['zoo', 'animals', 'cowoncy']):
                    zoo_messages.append(msg.content)
        
        if zoo_messages:
            zoo_data = await parse_zoo_message(zoo_messages)
            return zoo_data
        else:
            print("No zoo messages found")
            return None
            
    except Exception as e:
        print(f"Error fetching zoo data: {e}")
        import traceback
        print(traceback.format_exc())
        return None
    
async def parse_gems(inventory_message):
    rarity_order = ['f', 'l', 'm', 'e', 'r', 'u', 'c']
    gems_by_tier = {
        '1': [],
        '2': [],
        '3': [],
        '4': []
    }
    lines = inventory_message.split('\n')
    for line in lines:
        for tier in ['1', '2', '3', '4']:
            for rarity in rarity_order:
                pattern = fr'`(\d+)`<a?:({rarity}gem{tier}):\d+>'
                match = re.search(pattern, line)
                if match:
                    gem_number = match.group(1)
                    gems_by_tier[tier].append((rarity, gem_number))
    for tier in gems_by_tier:
        gems_by_tier[tier].sort(key=lambda x: rarity_order.index(x[0]))
    selected_gems = []
    for tier in ['1', '2', '3', '4']:
        if gems_by_tier[tier]:
            selected_gems.append(gems_by_tier[tier][0][1])

    return selected_gems
