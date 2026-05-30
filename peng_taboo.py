# -*- coding: utf-8 -*-
"""
彭祖百忌白話解釋（幽默現代版）
"""

PENG_TABOO_EXPLAIN = {
    # === 天干 ===
    "甲不開倉": "甲日別亂開錢包借錢給人，否則錢財跟你說掰掰",
    "乙不栽植": "乙日種什麼死什麼，連仙人掌都救不了",
    "丙不修灶": "丙日修廚房小心炸廚房，外賣比較安全",
    "丁不剃頭": "丁日剪頭髮會變醜，忍一天再去美容院",
    "戊不受田": "戊日別買房買地，小心踩雷",
    "己不破券": "己日別簽合約、別撕票，否則後悔莫及",
    "庚不經絡": "庚日別按摩針灸，小心越按越痠",
    "辛不合醬": "辛日別釀酒做醬，小心整缸報銷",
    "壬不泱水": "壬日別玩水游泳，小心喝飽",
    "癸不詞訟": "癸日別打官司告狀，穩輸的",

    # === 地支 ===
    "子不問卜": "子日別算命求籤，本來沒事反而自己嚇自己",
    "丑不冠帶": "丑日別穿新衣打扮，穿了也不好看",
    "寅不祭祀": "寅日拜拜沒誠意，神明假裝沒聽到",
    "卯不穿井": "卯日別挖井，挖了也是枯井",
    "辰不哭泣": "辰日別哭，哭了事情也不會變好",
    "巳不遠行": "巳日別出遠門，小心迷路回不來",
    "午不苫蓋": "午日別蓋屋頂修房子，小心漏雨",
    "未不服藥": "未日別吃藥，吃了也白吃",
    "申不安床": "申日別搬床換床位，否則失眠到天亮",
    "酉不會客": "酉日別請客吃飯，請了也沒人來",
    "戌不吃犬": "戌日別吃狗肉（現代：別虧待毛小孩）",
    "亥不嫁娶": "亥日別結婚，否則婚姻坎坷"
}

def get_peng_taboo_explain(taboo_text):
    """解析彭祖百忌並返回白話解釋"""
    if not taboo_text:
        return []
    
    results = []
    # 用逗號或空格分割
    parts = taboo_text.replace(',', ' ').split()
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # 尋找匹配的解釋
        explained = False
        for key, explain in PENG_TABOO_EXPLAIN.items():
            if key in part:
                results.append({"original": part, "explain": explain})
                explained = True
                break
        if not explained:
            results.append({"original": part, "explain": ""})
    
    return results
