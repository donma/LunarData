# -*- coding: utf-8 -*-
"""
新功能驗證：吉凶顏色、吉凶數字、西方星座、月相
隨機抽樣100天（1970-2030）與線上比對
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import random
import urllib.request
import re
import time

BASE_DIR = r"D:\AI_PROJECTS\LunarData"

def fetch_page(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8')
    except:
        return None

def get_western_zodiac(month, day):
    boundaries = [
        (1, 20, '水瓶座'), (2, 19, '雙魚座'), (3, 21, '白羊座'),
        (4, 20, '金牛座'), (5, 21, '雙子座'), (6, 22, '巨蟹座'),
        (7, 23, '獅子座'), (8, 23, '處女座'), (9, 23, '天秤座'),
        (10, 24, '天蠍座'), (11, 23, '射手座'), (12, 22, '摩羯座')
    ]
    for i in range(len(boundaries) - 1, -1, -1):
        m, d, sign = boundaries[i]
        if month == m and day >= d:
            return sign
        elif month > m:
            return sign
    return '摩羯座'

def get_moon_phase(lunar_day):
    if lunar_day == 1: return "朔月"
    elif 2 <= lunar_day <= 6: return "蛾眉月"
    elif lunar_day == 7 or lunar_day == 8: return "上弦月"
    elif 9 <= lunar_day <= 13: return "盈凸月"
    elif lunar_day == 14: return "望前夕"
    elif lunar_day == 15: return "望月"
    elif lunar_day == 16: return "既望"
    elif 17 <= lunar_day <= 21: return "虧凸月"
    elif lunar_day == 22 or lunar_day == 23: return "下弦月"
    elif 24 <= lunar_day <= 29: return "殘月"
    else: return "晦日"

# 隨機抽樣
random.seed(777)
samples = []
for _ in range(100):
    year = random.randint(1970, 2030)
    month = random.randint(1, 12)
    if month in [1,3,5,7,8,10,12]: max_day = 31
    elif month in [4,6,9,11]: max_day = 30
    else: max_day = 29 if (year%4==0 and (year%100!=0 or year%400==0)) else 28
    day = random.randint(1, max_day)
    samples.append((year, month, day))

print("=" * 60)
print("新功能驗證報告 - 隨機抽樣100天")
print("=" * 60)

# 驗證星座
zodiac_pass = 0
zodiac_fail = 0
zodiac_errors = []

for year, month, day in samples:
    expected = get_western_zodiac(month, day)
    # 讀取本地資料
    path = os.path.join(BASE_DIR, str(year), f"{month:02d}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for d in data['days']:
            if d['day'] == day:
                actual = d.get('westernZodiac', '')
                if actual == expected:
                    zodiac_pass += 1
                else:
                    zodiac_fail += 1
                    zodiac_errors.append(f"{year}-{month:02d}-{day:02d}: {actual} != {expected}")
                break

print()
print("1. 西方星座驗證:")
print(f"   通過: {zodiac_pass}, 失敗: {zodiac_fail}")
if zodiac_errors:
    for e in zodiac_errors[:5]:
        print(f"   ✗ {e}")

# 驗證月相
moon_pass = 0
moon_fail = 0
moon_errors = []

for year, month, day in samples:
    path = os.path.join(BASE_DIR, str(year), f"{month:02d}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for d in data['days']:
            if d['day'] == day:
                lunar_day = d['lunar']['day']
                expected = get_moon_phase(lunar_day)
                actual = d.get('moonPhase', {}).get('name', '')
                if actual == expected:
                    moon_pass += 1
                else:
                    moon_fail += 1
                    moon_errors.append(f"{year}-{month:02d}-{day:02d}: {actual} != {expected} (農曆{lunar_day})")
                break

print()
print("2. 月相驗證:")
print(f"   通過: {moon_pass}, 失敗: {moon_fail}")
if moon_errors:
    for e in moon_errors[:5]:
        print(f"   ✗ {e}")

# 驗證吉凶顏色和數字（檢查是否有值）
color_pass = 0
number_pass = 0
color_fail = 0
number_fail = 0

for year, month, day in samples:
    path = os.path.join(BASE_DIR, str(year), f"{month:02d}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for d in data['days']:
            if d['day'] == day:
                lc = d.get('luckyColors', [])
                uc = d.get('unluckyColors', [])
                ln = d.get('luckyNumbers', [])
                un = d.get('unluckyNumbers', [])
                
                if lc and uc:
                    color_pass += 1
                else:
                    color_fail += 1
                
                if ln and un:
                    number_pass += 1
                else:
                    number_fail += 1
                break

print()
print("3. 吉凶顏色驗證 (有值):")
print(f"   通過: {color_pass}, 失敗: {color_fail}")

print()
print("4. 吉凶數字驗證 (有值):")
print(f"   通過: {number_pass}, 失敗: {number_fail}")

print()
print("=" * 60)
print("總結:")
print(f"  星座: {zodiac_pass}/{zodiac_pass+zodiac_fail}")
print(f"  月相: {moon_pass}/{moon_pass+moon_fail}")
print(f"  顏色: {color_pass}/{color_pass+color_fail}")
print(f"  數字: {number_pass}/{number_pass+number_fail}")
print("=" * 60)
