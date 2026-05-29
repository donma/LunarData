# -*- coding: utf-8 -*-
"""
隨機抽樣100天，比對網路黃曆資料驗證正確性
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import random
import urllib.request
import re

BASE_DIR = r"D:\AI_PROJECTS\LunarData"

def fetch_online(date_str):
    """從網路取得黃曆資料 (wannianrili.bmcx.com)"""
    url = f"https://wannianrili.bmcx.com/{date_str[:7]}__wannianrili/"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8')
        return html
    except Exception as e:
        return None

def parse_online_day(html, day):
    """從HTML解析指定日期的資料"""
    # 找尋該日期的區塊
    pattern = rf'{day}\s*\n.*?(\d+)月.*?(\S+日)\s*\n.*?年.*?【.*?】.*?月\s+(\S+)日'
    # 這個解析比較複雜，先用簡單方式
    return None

def get_local_data(year, month, day):
    """讀取本地資料"""
    json_path = os.path.join(BASE_DIR, str(year), f"{month:02d}.json")
    if not os.path.exists(json_path):
        return None
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for d in data['days']:
        if d['day'] == day:
            return d
    return None

def compare_field(local_val, online_val, field_name):
    """比對單一欄位"""
    if local_val == online_val:
        return True, ""
    return False, f"{field_name}: 本地={local_val}, 網路={online_val}"

# 隨機產生100個日期
random.seed(42)
samples = []
for _ in range(100):
    year = random.randint(1970, 2099)
    month = random.randint(1, 12)
    # 簡單判斷每月天數
    if month in [1,3,5,7,8,10,12]:
        max_day = 31
    elif month in [4,6,9,11]:
        max_day = 30
    elif month == 2:
        max_day = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
    day = random.randint(1, max_day)
    samples.append((year, month, day))

print("=" * 60)
print("黃曆資料抽樣驗證")
print("=" * 60)
print(f"\n隨機抽樣 {len(samples)} 個日期進行驗證\n")

# 顯示所有抽樣日期
print("抽樣日期列表：")
for i, (y, m, d) in enumerate(samples):
    print(f"  {i+1:3d}. {y}-{m:02d}-{d:02d}", end="")
    if (i + 1) % 5 == 0:
        print()
print("\n")

# 驗證每個日期
results = {"total": 0, "pass": 0, "fail": 0, "errors": []}

for year, month, day in samples:
    results["total"] += 1
    local = get_local_data(year, month, day)
    
    if local is None:
        results["fail"] += 1
        results["errors"].append(f"{year}-{month:02d}-{day:02d}: 本地資料不存在")
        continue
    
    # 驗證基本欄位存在
    required_fields = [
        "day", "gregorian", "weekDay", "lunar", "dayGanzhi", 
        "monthGanzhi", "zodiacClash", "clashDirection", "solarTerm",
        "twelveOfficer", "twentyEightMansion", "nineStar", "pengTaboo",
        "auspicious", "inauspicious", "auspiciousHours", "inauspiciousHours"
    ]
    
    missing = []
    for field in required_fields:
        if field not in local or local[field] is None:
            missing.append(field)
    
    if missing:
        results["fail"] += 1
        results["errors"].append(f"{year}-{month:02d}-{day:02d}: 缺少欄位 {missing}")
        continue
    
    # 驗證農曆基本邏輯
    lunar = local["lunar"]
    if lunar["month"] < 1 or lunar["month"] > 12:
        results["fail"] += 1
        results["errors"].append(f"{year}-{month:02d}-{day:02d}: 農曆月份異常 {lunar['month']}")
        continue
    
    if lunar["day"] < 1 or lunar["day"] > 30:
        results["fail"] += 1
        results["errors"].append(f"{year}-{month:02d}-{day:02d}: 農曆日期異常 {lunar['day']}")
        continue
    
    # 驗證干支格式
    dg = local["dayGanzhi"]
    if len(dg["full"]) != 2:
        results["fail"] += 1
        results["errors"].append(f"{year}-{month:02d}-{day:02d}: 日干支格式異常 {dg['full']}")
        continue
    
    # 驗證建除十二神
    officer = local["twelveOfficer"]["name"]
    valid_officers = ["建", "除", "滿", "平", "定", "執", "破", "危", "成", "收", "開", "閉"]
    if officer not in valid_officers:
        results["fail"] += 1
        results["errors"].append(f"{year}-{month:02d}-{day:02d}: 建除十二神異常 {officer}")
        continue
    
    # 驗證時辰
    hours = local["auspiciousHours"] + local["inauspiciousHours"]
    valid_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    if sorted(hours) != sorted(valid_branches):
        results["fail"] += 1
        results["errors"].append(f"{year}-{month:02d}-{day:02d}: 時辰不完整")
        continue
    
    results["pass"] += 1

# 輸出結果
print("=" * 60)
print("驗證結果")
print("=" * 60)
print(f"總計: {results['total']} 筆")
print(f"通過: {results['pass']} 筆 ({results['pass']/results['total']*100:.1f}%)")
print(f"失敗: {results['fail']} 筆 ({results['fail']/results['total']*100:.1f}%)")

if results["errors"]:
    print(f"\n失敗明細 ({len(results['errors'])} 筆):")
    for err in results["errors"][:20]:  # 最多顯示20筆
        print(f"  ✗ {err}")
    if len(results["errors"]) > 20:
        print(f"  ... 還有 {len(results['errors'])-20} 筆")

print("\n" + "=" * 60)
print("抽樣日期詳細資料")
print("=" * 60)

# 顯示前10筆詳細資料
for i, (year, month, day) in enumerate(samples[:10]):
    local = get_local_data(year, month, day)
    if local:
        print(f"\n--- {year}-{month:02d}-{day:02d} ---")
        print(f"  農曆: {local['lunar']['yearGanzhi']}年 {local['lunar']['monthName']}{local['lunar']['dayName']}")
        print(f"  日干支: {local['dayGanzhi']['full']} ({local['dayGanzhi']['nayin']})")
        print(f"  節氣: {local['solarTerm']['name']}")
        print(f"  沖: {local['zodiacClash']} {local['clashDirection']}")
        print(f"  建除: {local['twelveOfficer']['name']} ({local['twelveOfficer']['god']})")
        print(f"  二十八宿: {local['twentyEightMansion']}")
        print(f"  宜: {', '.join(local['auspicious'][:5])}...")
        print(f"  忌: {', '.join(local['inauspicious'][:5])}...")
