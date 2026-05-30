# -*- coding: utf-8 -*-
"""
驗證建除十二神、二十八宿、九星
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import re
import urllib.request
import time
import random

BASE_DIR = r"D:\AI_PROJECTS\LunarData"

# 簡繁轉換
S2T = {
    '闭':'閉','开':'開','建':'建','除':'除','满':'滿','平':'平',
    '定':'定','执':'執','破':'破','危':'危','成':'成','收':'收',
    '角':'角','亢':'亢','氐':'氐','房':'房','心':'心','尾':'尾',
    '箕':'箕','斗':'斗','牛':'牛','女':'女','虛':'虛','虚':'虛',
    '危':'危','室':'室','壁':'壁','奎':'奎','婁':'婁','娄':'婁',
    '胃':'胃','昴':'昴','畢':'畢','毕':'畢','觜':'觜','參':'參',
    '参':'參','井':'井','鬼':'鬼','柳':'柳','星':'星','張':'張',
    '张':'張','翼':'翼','軫':'軫','轸':'軫',
    '青龍':'青龍','青龙':'青龍','明堂':'明堂','天刑':'天刑',
    '朱雀':'朱雀','金匱':'金匱','金匮':'金匱','天德':'天德',
    '白虎':'白虎','玉堂':'玉堂','天牢':'天牢','玄武':'玄武',
    '司命':'司命','勾陳':'勾陳','勾陈':'勾陳',
}

def s2t(text):
    if not text: return text
    for s, t in S2T.items():
        text = text.replace(s, t)
    return text

def fetch_page(url):
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode('utf-8')
    except:
        return None

def parse_online_detail(html, target_day):
    """解析線上黃曆詳細資訊"""
    if not html: return None
    
    # 找 "XX日 详细信息" 格式 - 更寬鬆的匹配
    pattern = rf'月{target_day:02d}日\s*详细信息(.*?)(?=月\d{{2}}日\s*详细信息|$)'
    m = re.search(pattern, html, re.DOTALL)
    if not m:
        # 嘗試另一種格式
        pattern2 = rf'{target_day:02d}日\s*详细信息(.*?)(?=\d{{2}}日\s*详细信息|$)'
        m = re.search(pattern2, html, re.DOTALL)
    
    if not m: return None
    
    info = m.group(1)
    result = {}
    
    # 十二神: "十二神闭执位"
    officer = re.search(r'十二神(\S+?)执位', info)
    if officer:
        result['officer'] = s2t(officer.group(1))
    
    # 星宿: "星宿房宿（房日兔）"
    star = re.search(r'星宿\S+?宿（(\S+?)）', info)
    if star:
        result['star28'] = s2t(star.group(1))
    
    return result

def get_local(year, month, day):
    path = os.path.join(BASE_DIR, str(year), f"{month:02d}.json")
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for d in data['days']:
        if d['day'] == day:
            return d
    return None

# 主程式
print("=" * 60)
print("驗證建除十二神 & 二十八宿")
print("=" * 60)

random.seed(999)
samples = []
for _ in range(100):
    year = random.randint(2026, 2099)
    month = random.randint(1, 12)
    if month in [1,3,5,7,8,10,12]: max_day = 31
    elif month in [4,6,9,11]: max_day = 30
    else: max_day = 28
    day = random.randint(1, max_day)
    samples.append((year, month, day))

from collections import defaultdict
grouped = defaultdict(list)
for y, m, d in samples:
    grouped[(y, m)].append(d)

officer_pass = 0
officer_fail = 0
star_pass = 0
star_fail = 0
errors = []

for (year, month), days in sorted(grouped.items()):
    url = f"https://wannianrili.bmcx.com/{year}-{month:02d}__wannianrili/"
    html = fetch_page(url)
    time.sleep(0.2)
    
    if not html:
        continue
    
    for day in sorted(days):
        local = get_local(year, month, day)
        online = parse_online_detail(html, day)
        
        if not local or not online:
            continue
        
        # 比對十二神
        if online.get('officer'):
            local_officer = local.get('twelveOfficer', {}).get('name', '')
            online_officer = online['officer']
            if local_officer == online_officer:
                officer_pass += 1
            else:
                officer_fail += 1
                errors.append(f"{year}-{month:02d}-{day:02d} officer: {local_officer} != {online_officer}")
        
        # 比對二十八宿
        if online.get('star28'):
            local_star = local.get('twentyEightMansion', '')
            online_star = online['star28']
            if local_star == online_star:
                star_pass += 1
            else:
                star_fail += 1
                errors.append(f"{year}-{month:02d}-{day:02d} star28: {local_star} != {online_star}")

print()
print("驗證結果:")
print(f"  建除十二神: 通過={officer_pass} 失敗={officer_fail}")
print(f"  二十八宿:   通過={star_pass} 失敗={star_fail}")

if errors:
    print()
    print("失敗明細:")
    for e in errors[:20]:
        print(f"  {e}")
