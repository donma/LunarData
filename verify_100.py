# -*- coding: utf-8 -*-
"""
黃曆資料驗證腳本 - 抽樣100天與線上黃曆比對
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import random
import re
import urllib.request
import time

BASE_DIR = r"D:\AI_PROJECTS\LunarData"

def fetch_online(year, month):
    url = f"https://wannianrili.bmcx.com/{year}-{month:02d}__wannianrili/"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode('utf-8')
        return html
    except Exception as e:
        print(f'    Fetch error: {e}')
        return None

def parse_day_from_html(html, target_day):
    if not html:
        return None
    
    # 格式: "2026月05月30日 详细信息...冲狗 （戊戌）煞南..."
    # 用更寬鬆的匹配
    pattern = rf'月{target_day:02d}日\s*详细信息(.*?)(?=月\d{{2}}日\s*详细信息|$)'
    m = re.search(pattern, html, re.DOTALL)
    
    if not m:
        # 嘗試另一種格式
        pattern2 = rf'{target_day:02d}日\s*详细信息(.*?)(?=\d{{2}}日\s*详细信息|$)'
        m = re.search(pattern2, html, re.DOTALL)
    
    if not m:
        return None
    
    info = m.group(1)
    result = {}
    
    # 沖煞: "冲X （干支）煞Y"
    clash = re.search(r'冲(\S+)\s*（(\S+)）\s*煞(\S+)', info)
    if clash:
        result['zodiac'] = clash.group(1)
        result['ganzhi'] = clash.group(2)
        result['direction'] = clash.group(3)
    
    # 彭祖
    peng = re.search(r'彭祖百忌(\S+?)胎', info)
    if peng:
        result['peng'] = peng.group(1).strip()
    
    return result
    
    # 找 "X月X日 详细信息" 格式的區塊
    pattern = r'(\d{2})月(\d{2})日\s*详细信息(.*?)(?=\d{2}月\d{2}日\s*详细信息|$)'
    matches = list(re.finditer(pattern, html, re.DOTALL))
    
    for m in matches:
        day = int(m.group(2))
        if day == target_day:
            info = m.group(3)
            result = {}
            
            # 沖煞: "冲X （干支）煞Y"
            clash = re.search(r'冲(\S+)\s*[（(](\S+)[）)]\s*煞(\S+)', info)
            if clash:
                result['zodiac'] = clash.group(1)
                result['ganzhi'] = clash.group(2)
                result['direction'] = clash.group(3)
            
            # 彭祖
            peng = re.search(r'彭祖百忌(\S+?)胎', info)
            if peng:
                result['peng'] = peng.group(1).strip()
            
            # 日干支 (從 "X月X日" 前面的干支)
            # 格式: 四月十四丙午年 【马年】 癸巳月 甲辰日
            gz = re.search(r'(\S{2})日', info[:30])
            if gz:
                result['dayGanzhi'] = gz.group(1)
            
            return result
    return None

def get_local(year, month, day):
    path = os.path.join(BASE_DIR, str(year), f"{month:02d}.json")
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for d in data['days']:
        if d['day'] == day:
            return d
    return None

# 主程式
print("=" * 70)
print("黃曆資料驗證報告 - 隨機抽樣100天")
print("=" * 70)

random.seed(2026)
samples = []
for _ in range(100):
    year = random.randint(2026, 2099)
    month = random.randint(1, 12)
    if month in [1,3,5,7,8,10,12]: max_day = 31
    elif month in [4,6,9,11]: max_day = 30
    else: max_day = 29 if (year%4==0 and (year%100!=0 or year%400==0)) else 28
    day = random.randint(1, max_day)
    samples.append((year, month, day))

# 按年月分組
from collections import defaultdict
grouped = defaultdict(list)
for y, m, d in samples:
    grouped[(y, m)].append(d)

results = {"pass": 0, "fail": 0, "skip": 0, "errors": []}
detail_results = []

for (year, month), days in sorted(grouped.items()):
    html = fetch_online(year, month)
    time.sleep(0.3)
    
    if not html:
        for d in days:
            results["skip"] += 1
            detail_results.append((year, month, d, "SKIP", "無法取得線上資料"))
        continue
    
    for day in sorted(days):
        local = get_local(year, month, day)
        online = parse_day_from_html(html, day)
        
        if not local:
            results["skip"] += 1
            detail_results.append((year, month, day, "SKIP", "本地資料不存在"))
            continue
        
        if not online:
            results["skip"] += 1
            detail_results.append((year, month, day, "SKIP", "無法解析線上資料"))
            continue
        
        # 比對沖煞生肖
        if online.get('zodiac'):
            local_z = local.get('zodiacClash', '')
            online_z = online['zodiac']
            if local_z == online_z:
                results["pass"] += 1
                detail_results.append((year, month, day, "PASS", f"沖{local_z}"))
            else:
                results["fail"] += 1
                msg = f"沖: 本地={local_z} 線上={online_z}"
                results["errors"].append(f"{year}-{month:02d}-{day:02d}: {msg}")
                detail_results.append((year, month, day, "FAIL", msg))
        
        # 比對煞方位
        if online.get('direction'):
            local_d = local.get('clashDirection', '')
            online_d = online['direction']
            dir_map = {'东':'東','南':'南','西':'西','北':'北'}
            online_d_t = dir_map.get(online_d, online_d)
            if local_d == online_d_t:
                results["pass"] += 1
            else:
                results["fail"] += 1
                msg = f"煞: 本地={local_d} 線上={online_d_t}"
                results["errors"].append(f"{year}-{month:02d}-{day:02d}: {msg}")

# 輸出報告
print(f"\n{'='*70}")
print("驗證結果總結")
print(f"{'='*70}")
total = results["pass"] + results["fail"]
print(f"通過: {results['pass']}")
print(f"失敗: {results['fail']}")
print(f"跳過: {results['skip']}")
if total > 0:
    print(f"準確率: {results['pass']/total*100:.1f}%")

if results["errors"]:
    print(f"\n失敗明細:")
    for err in results["errors"][:30]:
        print(f"  ✗ {err}")

print(f"\n{'='*70}")
print("抽樣驗證明細")
print(f"{'='*70}")
for year, month, day, status, msg in detail_results[:50]:
    symbol = "✓" if status == "PASS" else "✗" if status == "FAIL" else "○"
    print(f"  {symbol} {year}-{month:02d}-{day:02d}: {msg}")
