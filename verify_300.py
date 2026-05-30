# -*- coding: utf-8 -*-
"""
三派宜忌驗證腳本
驗證建除十二神派、天星擇日派、紫白九星派各100天
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import random

BASE_DIR = r"D:\AI_PROJECTS\LunarData"

# ============================
# 建除十二神派標準宜忌
# ============================
JIANCHU_STANDARD = {
    "建": {"yi": ["出行","上任","赴任"], "ji": ["動土","開倉"]},
    "除": {"yi": ["解除","沐浴","掃舍"], "ji": ["嫁娶","出行"]},
    "滿": {"yi": ["嫁娶","移徙","開市"], "ji": ["動土","安葬"]},
    "平": {"yi": ["修造","動土"], "ji": ["嫁娶","出行"]},
    "定": {"yi": ["冠笄","嫁娶","納采"], "ji": ["詞訟","出行"]},
    "執": {"yi": ["捕捉","祭祀"], "ji": ["移徙","開市"]},
    "破": {"yi": ["破屋","壞垣"], "ji": ["嫁娶","開市"]},
    "危": {"yi": ["祭祀","祈福"], "ji": ["登高","遠行"]},
    "成": {"yi": ["嫁娶","開市","交易"], "ji": ["詞訟"]},
    "收": {"yi": ["納財","收債"], "ji": ["安葬","動土"]},
    "開": {"yi": ["開市","出行","嫁娶"], "ji": ["安葬","動土"]},
    "閉": {"yi": ["安葬","納財"], "ji": ["開市","出行"]}
}

# ============================
# 天星擇日派標準宜忌（二十八宿）
# ============================
STAR28_STANDARD = {
    "角": {"yi": ["嫁娶","出行","建造"], "ji": ["安葬"]},
    "亢": {"yi": ["祭祀","安葬"], "ji": ["嫁娶","出行"]},
    "氐": {"yi": ["祭祀","安葬"], "ji": ["嫁娶","動土"]},
    "房": {"yi": ["嫁娶","開市","出行"], "ji": ["安葬"]},
    "心": {"yi": ["祭祀"], "ji": ["嫁娶","建造"]},
    "尾": {"yi": ["嫁娶","造作","開市"], "ji": ["安葬"]},
    "箕": {"yi": ["開市","嫁娶","出行"], "ji": ["安葬"]},
    "斗": {"yi": ["建造","嫁娶","開市"], "ji": ["安葬"]},
    "牛": {"yi": ["祭祀"], "ji": ["嫁娶","動土"]},
    "女": {"yi": ["祭祀"], "ji": ["開市","嫁娶"]},
    "虛": {"yi": [], "ji": ["百事不宜"]},
    "危": {"yi": ["祭祀","安床"], "ji": ["登高","遠行"]},
    "室": {"yi": ["建造","嫁娶","開市"], "ji": []},
    "壁": {"yi": ["建造","納財","開市"], "ji": ["安葬"]},
    "奎": {"yi": ["開市","遠行","建造"], "ji": ["安葬"]},
    "婁": {"yi": ["嫁娶","造葬","開市"], "ji": []},
    "胃": {"yi": ["嫁娶","造葬","開市"], "ji": []},
    "昴": {"yi": ["祭祀"], "ji": ["造葬","遠行"]},
    "畢": {"yi": ["造葬","開市","建造"], "ji": ["遠行"]},
    "觜": {"yi": ["祭祀"], "ji": ["造葬","動土"]},
    "參": {"yi": ["祭祀"], "ji": ["造葬","出行"]},
    "井": {"yi": ["開市","嫁娶","建造"], "ji": ["安葬"]},
    "鬼": {"yi": ["祭祀","安葬"], "ji": ["百事不宜"]},
    "柳": {"yi": ["祭祀"], "ji": ["造葬","開市"]},
    "星": {"yi": ["祭祀"], "ji": ["造葬","開市"]},
    "張": {"yi": ["嫁娶","開市","出行"], "ji": ["安葬"]},
    "翼": {"yi": ["祭祀"], "ji": ["造葬","遠行"]},
    "軫": {"yi": ["建造","遠行","開市"], "ji": ["安葬"]}
}

# ============================
# 紫白九星派標準宜忌
# ============================
JIUBAI_STANDARD = {
    "1": {"yi": ["求財","嫁娶","出行"], "ji": []},
    "2": {"yi": ["祭祀","求醫"], "ji": ["動土","開市"]},
    "3": {"yi": [], "ji": ["嫁娶","開市","出行"]},
    "4": {"yi": ["入學","考試","求官"], "ji": []},
    "5": {"yi": [], "ji": ["百事不宜"]},
    "6": {"yi": ["求財","開市","出行"], "ji": []},
    "7": {"yi": [], "ji": ["開市","嫁娶","出行"]},
    "8": {"yi": ["求財","開市","嫁娶"], "ji": []},
    "9": {"yi": ["嫁娶","開市","出行"], "ji": []}
}

def check_subset(actual, standard):
    """檢查實際宜忌是否包含標準項目"""
    if not standard:
        return True, 0, 0
    actual_set = set(actual)
    standard_set = set(standard)
    match = len(actual_set & standard_set)
    total = len(standard_set)
    return match > 0, match, total

def verify_day(d):
    """驗證一天的三派宜忌"""
    results = {"jianchu": {}, "tianxing": {}, "jiubai": {}}
    
    ts = d.get('threeSchools', {}) or {}
    
    # 1. 建除十二神派
    jianchu = ts.get('jianchu') or {}
    officer = d.get('twelveOfficer', {}).get('name', '')
    if officer in JIANCHU_STANDARD:
        std = JIANCHU_STANDARD[officer]
        actual_yi = jianchu.get('yi', [])
        actual_ji = jianchu.get('ji', [])
        
        yi_ok, yi_match, yi_total = check_subset(actual_yi, std['yi'])
        ji_ok, ji_match, ji_total = check_subset(actual_ji, std['ji'])
        
        results['jianchu'] = {
            'officer': officer,
            'yi_pass': yi_ok,
            'yi_match': yi_match,
            'yi_total': yi_total,
            'ji_pass': ji_ok,
            'ji_match': ji_match,
            'ji_total': ji_total
        }
    
    # 2. 天星擇日派
    tianxing = ts.get('tianxing') or {}
    star28 = d.get('twentyEightMansion', '')
    star_short = star28[0] if star28 else ''
    if star_short in STAR28_STANDARD:
        std = STAR28_STANDARD[star_short]
        actual_yi = tianxing.get('yi', [])
        actual_ji = tianxing.get('ji', [])
        
        yi_ok, yi_match, yi_total = check_subset(actual_yi, std['yi'])
        ji_ok, ji_match, ji_total = check_subset(actual_ji, std['ji'])
        
        results['tianxing'] = {
            'star': star28,
            'yi_pass': yi_ok,
            'yi_match': yi_match,
            'yi_total': yi_total,
            'ji_pass': ji_ok,
            'ji_match': ji_match,
            'ji_total': ji_total
        }
    
    # 3. 紫白九星派
    jiubai = ts.get('jiubai') or {}
    nine_star = d.get('nineStar', '')
    center_star = nine_star[0] if nine_star else ''
    if center_star in JIUBAI_STANDARD:
        std = JIUBAI_STANDARD[center_star]
        actual_yi = jiubai.get('yi', [])
        actual_ji = jiubai.get('ji', [])
        
        yi_ok, yi_match, yi_total = check_subset(actual_yi, std['yi'])
        ji_ok, ji_match, ji_total = check_subset(actual_ji, std['ji'])
        
        results['jiubai'] = {
            'star': center_star,
            'yi_pass': yi_ok,
            'yi_match': yi_match,
            'yi_total': yi_total,
            'ji_pass': ji_ok,
            'ji_match': ji_match,
            'ji_total': ji_total
        }
    
    return results

# 主程式
print("=" * 70)
print("三派宜忌驗證報告 - 隨機抽樣100天")
print("=" * 70)

random.seed(456)
samples = []
for _ in range(100):
    year = random.randint(2026, 2099)
    month = random.randint(1, 12)
    if month in [1,3,5,7,8,10,12]: max_day = 31
    elif month in [4,6,9,11]: max_day = 30
    else: max_day = 28
    day = random.randint(1, max_day)
    samples.append((year, month, day))

# 統計
stats = {
    'jianchu': {'yi_pass': 0, 'yi_fail': 0, 'ji_pass': 0, 'ji_fail': 0},
    'tianxing': {'yi_pass': 0, 'yi_fail': 0, 'ji_pass': 0, 'ji_fail': 0},
    'jiubai': {'yi_pass': 0, 'yi_fail': 0, 'ji_pass': 0, 'ji_fail': 0}
}
errors = []

for year, month, day in samples:
    path = os.path.join(BASE_DIR, str(year), f"{month:02d}.json")
    if not os.path.exists(path):
        continue
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    d = None
    for dd in data['days']:
        if dd['day'] == day:
            d = dd
            break
    
    if not d:
        continue
    
    results = verify_day(d)
    
    for school in ['jianchu', 'tianxing', 'jiubai']:
        r = results[school]
        if r:
            if r.get('yi_pass'):
                stats[school]['yi_pass'] += 1
            else:
                stats[school]['yi_fail'] += 1
                if r.get('yi_total', 0) > 0:
                    errors.append(f"{year}-{month:02d}-{day:02d} {school} yi fail: {r.get('yi_match',0)}/{r.get('yi_total',0)}")
            
            if r.get('ji_pass'):
                stats[school]['ji_pass'] += 1
            else:
                stats[school]['ji_fail'] += 1
                if r.get('ji_total', 0) > 0:
                    errors.append(f"{year}-{month:02d}-{day:02d} {school} ji fail: {r.get('ji_match',0)}/{r.get('ji_total',0)}")

print()
print("驗證結果:")
print("-" * 50)
for school, name in [('jianchu','建除十二神派'), ('tianxing','天星擇日派'), ('jiubai','紫白九星派')]:
    s = stats[school]
    yi_total = s['yi_pass'] + s['yi_fail']
    ji_total = s['ji_pass'] + s['ji_fail']
    yi_rate = s['yi_pass'] / yi_total * 100 if yi_total > 0 else 0
    ji_rate = s['ji_pass'] / ji_total * 100 if ji_total > 0 else 0
    print(f"  {name}:")
    print(f"    宜: {s['yi_pass']}/{yi_total} ({yi_rate:.0f}%)")
    print(f"    忌: {s['ji_pass']}/{ji_total} ({ji_rate:.0f}%)")

if errors:
    print()
    print("失敗明細 (前10項):")
    for e in errors[:10]:
        print(f"  {e}")

print()
print("=" * 70)
print("說明:")
print("- 建除十二神派: 以十二值日定吉凶")
print("- 天星擇日派: 以二十八宿定吉凶")
print("- 紫白九星派: 以九宮飛星定吉凶")
print("- 三派算法不同，宜忌項目會有差異，此為正常現象")
print("=" * 70)
