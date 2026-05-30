# -*- coding: utf-8 -*-
"""
黃曆資料驗證腳本
隨機抽樣100天，與線上黃曆比對
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import random
import re
import urllib.request

BASE_DIR = r"D:\AI_PROJECTS\LunarData"

def fetch_online(year, month):
    """從線上取得黃曆資料"""
    url = f"https://wannianrili.bmcx.com/{year}-{month:02d}__wannianrili/"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8')
        return html
    except Exception as e:
        return None

def parse_online_day(html, day):
    """從HTML解析指定日期的資料"""
    if not html:
        return None
    
    # 找尋日期區塊的詳細資訊
    # 格式: 2026月05月30日 详细信息
    pattern = rf'(\d{{4}})月(\d{{2}})月(\d{{2}})日\s*详细信息(.*?)(?=\d{{4}}月\d{{2}}月\d{{2}}日\s*详细信息|$)'
    matches = re.findall(pattern, html, re.DOTALL)
    
    for match in matches:
        y, m, d = int(match[0]), int(match[1]), int(match[2])
        if d == day:
            info = match[3]
            
            # 解析沖煞
            clash_match = re.search(r'冲(\S+)\s*（(\S+)）\s*煞(\S+)', info)
            clash_zodiac = clash_match.group(1) if clash_match else ''
            clash_ganzhi = clash_match.group(2) if clash_match else ''
            clash_dir = clash_match.group(3) if clash_match else ''
            
            # 解析日干支 - 從 "X月X日" 後面找
            day_gz_match = re.search(r'(\S+)日', info[:20])
            day_ganzhi = ''
            
            # 解析彭祖
            peng_match = re.search(r'彭祖百忌(\S+)', info)
            peng = peng_match.group(1) if peng_match else ''
            
            # 解析宜忌
            yi_match = re.search(r'宜(.*?)忌', info, re.DOTALL)
            ji_match = re.search(r'忌(.*?)$', info, re.DOTALL)
            yi_items = []
            ji_items = []
            if yi_match:
                yi_text = yi_match.group(1).strip()
                yi_items = [x.strip() for x in re.split(r'\s+', yi_text) if x.strip()]
            if ji_match:
                ji_text = ji_match.group(1).strip()
                ji_items = [x.strip() for x in re.split(r'\s+', ji_text) if x.strip()]
            
            return {
                'clash_zodiac': clash_zodiac,
                'clash_ganzhi': clash_ganzhi,
                'clash_dir': clash_dir,
                'peng': peng,
                'yi': yi_items[:5],  # 只取前5個比對
                'ji': ji_items[:5]
            }
    
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

def compare_data(local, online, year, month, day):
    """比對本地和線上資料"""
    results = []
    
    if not local:
        return [('ERROR', '本地資料不存在')]
    
    if not online:
        return [('SKIP', '無法取得線上資料')]
    
    # 比對沖煞生肖
    local_zodiac = local.get('zodiacClash', '')
    online_zodiac = online.get('clash_zodiac', '')
    if local_zodiac and online_zodiac:
        if local_zodiac == online_zodiac:
            results.append(('PASS', f'沖: {local_zodiac} = {online_zodiac}'))
        else:
            results.append(('FAIL', f'沖: {local_zodiac} != {online_zodiac}'))
    
    # 比對煞方位
    local_dir = local.get('clashDirection', '')
    online_dir = online.get('clash_dir', '')
    dir_map = {'东': '東', '南': '南', '西': '西', '北': '北'}
    online_dir_t = dir_map.get(online_dir, online_dir)
    if local_dir and online_dir_t:
        if local_dir == online_dir_t:
            results.append(('PASS', f'煞: {local_dir} = {online_dir_t}'))
        else:
            results.append(('FAIL', f'煞: {local_dir} != {online_dir_t}'))
    
    return results

# 主程式
print("=" * 60)
print("黃曆資料驗證 - 隨機抽樣100天")
print("=" * 60)

# 隨機產生100個日期
random.seed(42)
samples = []
for _ in range(100):
    year = random.randint(2026, 2099)
    month = random.randint(1, 12)
    if month in [1,3,5,7,8,10,12]:
        max_day = 31
    elif month in [4,6,9,11]:
        max_day = 30
    elif month == 2:
        max_day = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
    day = random.randint(1, max_day)
    samples.append((year, month, day))

print(f"\n抽樣 {len(samples)} 個日期進行驗證\n")

# 按年月分組以減少網路請求
from collections import defaultdict
grouped = defaultdict(list)
for y, m, d in samples:
    grouped[(y, m)].append(d)

total_pass = 0
total_fail = 0
total_skip = 0
errors = []

for (year, month), days in sorted(grouped.items()):
    print(f"正在驗證 {year}-{month:02d}...", end=" ")
    
    # 取得線上資料
    html = fetch_online(year, month)
    if not html:
        print(f"無法取得線上資料，跳過 {len(days)} 天")
        total_skip += len(days)
        continue
    
    month_pass = 0
    month_fail = 0
    
    for day in sorted(days):
        local = get_local_data(year, month, day)
        online = parse_online_day(html, day)
        
        results = compare_data(local, online, year, month, day)
        
        for status, msg in results:
            if status == 'PASS':
                total_pass += 1
                month_pass += 1
            elif status == 'FAIL':
                total_fail += 1
                month_fail += 1
                errors.append(f"{year}-{month:02d}-{day:02d}: {msg}")
            elif status == 'SKIP':
                total_skip += 1
    
    if month_fail == 0:
        print(f"✓ 通過 ({month_pass} 項)")
    else:
        print(f"✗ 失敗 {month_fail} 項, 通過 {month_pass} 項")

print("\n" + "=" * 60)
print("驗證結果總結")
print("=" * 60)
print(f"通過: {total_pass}")
print(f"失敗: {total_fail}")
print(f"跳過: {total_skip}")
print(f"準確率: {total_pass/(total_pass+total_fail)*100:.1f}%")

if errors:
    print(f"\n失敗明細 ({len(errors)} 項):")
    for err in errors[:20]:
        print(f"  ✗ {err}")
    if len(errors) > 20:
        print(f"  ... 還有 {len(errors)-20} 項")

print("\n" + "=" * 60)
print("抽樣日期詳細資料")
print("=" * 60)

# 顯示前10筆詳細資料
for year, month, day in samples[:10]:
    local = get_local_data(year, month, day)
    if local:
        print(f"\n--- {year}-{month:02d}-{day:02d} ---")
        print(f"  農曆: {local['lunar']['yearGanzhi']}年 {local['lunar']['monthName']}{local['lunar']['dayName']}")
        print(f"  日干支: {local['dayGanzhi']['full']} ({local['dayGanzhi']['nayin']})")
        print(f"  節氣: {local['solarTerm']['name']}")
        print(f"  沖: {local['zodiacClash']} {local['clashDirection']}")
        print(f"  建除: {local['twelveOfficer']['name']} ({local['twelveOfficer']['god']})")
        print(f"  二十八宿: {local['twentyEightMansion']}")
        print(f"  彭祖: {local['pengTaboo']}")
