"""
This code is only made for educational and practice purposes. 
Author and Fully Development are not responsible for misuse.

Fully OwO V4 Alpha Build
Stable Alpha Build Version: 110126.4.0.3

GitHub: https://github.com/fullygamerz
Discord: https://discord.com/user/fullyneverdies/
"""

# DO NOT CHANGE THIS FILE UNLESS YOU KNOW WHAT YOU'RE DOING 

import os
import requests
from PIL import Image
import numpy as np
from io import BytesIO

def fullyGetImgPaths(directory):
    results = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.png'):
                results.append(os.path.join(root, file))
    
    return results

def CompareAllImgsfullys(large_data, large_w, small_data, small_w, small_h, start_x, start_y):
    for y in range(small_h):
        for x in range(small_w):
            large_idx = ((start_y + y) * large_w + (start_x + x)) * 4
            small_idx = (y * small_w + x) * 4
            if (small_data[small_idx + 3] > 0 and 
                (small_data[small_idx] != large_data[large_idx] or
                 small_data[small_idx + 1] != large_data[large_idx + 1] or
                 small_data[small_idx + 2] != large_data[large_idx + 2])):
                return False
    
    return True

def MatchfullyCapLetters(large_data, large_w, large_h, checks):
    matches = []
    for check in checks:
        img_data = check['img_data']
        small_w = check['width']
        small_h = check['height']
        letter = check['letter']
        
        for y in range(large_h - small_h + 1):
            for x in range(large_w - small_w + 1):
                if CompareAllImgsfullys(large_data, large_w, img_data, small_w, small_h, x, y):
                    overlaps = any(
                        abs(match['x'] - x) < small_w and abs(match['y'] - y) < small_h
                        for match in matches
                    )
                    
                    if not overlaps:
                        matches.append({'x': x, 'y': y, 'letter': letter})
    matches.sort(key=lambda m: m['x'])
    return ''.join(match['letter'] for match in matches)

async def fullySolveNormalCap(captcha_url):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    letters_dir = os.path.join(current_dir, "letters")
    checks = []
    check_images = sorted(fullyGetImgPaths(letters_dir))
    
    for check_image_path in check_images:
        with Image.open(check_image_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            width, height = img.size
            img_array = np.array(img)
            img_data = img_array.flatten().astype(np.uint8)
            letter = os.path.splitext(os.path.basename(check_image_path))[0]
            
            checks.append({
                'img_data': img_data,
                'width': width,
                'height': height,
                'letter': letter
            })
    response = requests.get(captcha_url)
    response.raise_for_status()
    with Image.open(BytesIO(response.content)) as large_img:
        if large_img.mode != 'RGBA':
            large_img = large_img.convert('RGBA')
        
        width, height = large_img.size
        large_array = np.array(large_img)
        large_data = large_array.flatten().astype(np.uint8)
    return MatchfullyCapLetters(large_data, width, height, checks)

def fullySyncedCaptchaSolve(captcha_url):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    letters_dir = os.path.join(current_dir, "letters")
    checks = []
    check_images = sorted(fullyGetImgPaths(letters_dir))
    for check_image_path in check_images:
        with Image.open(check_image_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            width, height = img.size
            img_array = np.array(img)
            img_data = img_array.flatten().astype(np.uint8)
            letter = os.path.splitext(os.path.basename(check_image_path))[0]
            
            checks.append({
                'img_data': img_data,
                'width': width,
                'height': height,
                'letter': letter
            })
    

    response = requests.get(captcha_url)
    response.raise_for_status()
    

    with Image.open(BytesIO(response.content)) as large_img:

        if large_img.mode != 'RGBA':
            large_img = large_img.convert('RGBA')
        
        width, height = large_img.size

        large_array = np.array(large_img)
        large_data = large_array.flatten().astype(np.uint8)
    return MatchfullyCapLetters(large_data, width, height, checks)

if __name__ == "__main__":
    pass
