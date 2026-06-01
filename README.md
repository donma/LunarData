# 擇日知錄 - 農民曆

> 整合農曆、干支、節氣、宜忌、吉時、神明誕辰、彭祖百忌、九宮飛星與多種傳統曆法資訊，純前端即可查詢。
>
> 「我願稱之目前地表最強農民曆」

**[線上展示](https://donma.github.io/LunarData/)**

## 功能特色

### 黃曆核心
- 農曆 / 國曆轉換
- 天干地支（年柱、月柱、日柱）
- 生肖、沖煞方位、虛歲（依六十甲子精確計算）
- 二十四節氣（含白話註解）
- 宜 / 忌（含白話解釋 tooltip）
- 吉時 / 凶時（含時辰干支）
- 建除十二神
- 二十八宿（日宿法 + 月宿法雙算法）
- 九宮飛星（點擊進入詳解頁）
- 彭祖百忌（含幽默白話文解釋）
- 神明誕辰（130 位神明，含小知識介紹）

### 三派擇日
- **建除十二神派** — 以十二值日定吉凶
- **天星擇日派** — 參考二十八星宿運行
- **紫白九星派** — 結合九宮飛星與八卦

### 新增功能
- 每日吉凶顏色（依日干五行）
- 每日吉凶數字
- 西方星座（含 emoji）
- 月相顯示（朔望弦晦）
- 節季註解
- 喜神、財神、福神方位
- 胎神方位
- 生肖圖片（沖煞卡片背景）
- 泰國佛日參考資料區塊（規則推算版，附 1 天差異提醒）

### 特色節日
- **天穿日**（農曆正月二十）— 客家傳統節日，女媧補天紀念日
- **天赦日**（春戊寅、夏甲午、秋戊申、冬甲子）— 百無禁忌的黃道吉日
- **冷門國際節日** — 93 個西曆節日，包含國際壽司日、海盜說話日、醜毛衣日等趣味節日，並補上短版冷知識註解
- **農曆傳統節日** — 春節、端午、中秋、重陽、除夕等 12 個重要節日
- **泰國佛日參考資料** — 顯示泰國佛日、衛塞節、入雨安居等事件，採規則推算並明確標示參考性質

### 圖表總覽
- 📅 月曆總覽（點擊切換日期）
- 📊 本月吉凶比例（圓餅圖）
- 🔮 本月每日五行分布
- 🌀 節氣時間軸

### 九宮飛星詳解
- 洛書九宮圖
- 九星飛行順序
- 五行相生相剋圖解
- 三元九運時間表
- 各星詳細宜忌

## 資料範圍

| 項目 | 內容 |
|------|------|
| 年份 | 1970 ~ 2100（共 131 年） |
| 格式 | JSON + JS |
| 語言 | 繁體中文 |
| 準確度 | 100 筆隨機抽樣驗證通過 |

## 快速開始

### 方式一：直接開啟（推薦）

直接用瀏覽器開啟 `index.html`，無需安裝任何東西。

```
index.html          ← 主頁（黃曆查詢）
ninestar.html       ← 九宮飛星詳解
```

### 方式二：本地伺服器

```bash
python -m http.server 8080
```

然後訪問 http://localhost:8080

## 目錄結構

```
LunarData/
├── index.html              ← 主頁（黃曆查詢）
├── ninestar.html           ← 九宮飛星詳解
├── README.md               ← 本說明文件
├── LICENSE                 ← MIT 授權
├── .gitignore
│
├── generate.py             ← 資料產出腳本（僅開發用）
├── convert_to_js.py        ← JSON 轉 JS（僅開發用）
├── verify_100.py           ← 100天抽樣驗證（僅開發用）
├── verify_300.py           ← 三派宜忌驗證（僅開發用）
├── verify_new.py           ← 新功能驗證（僅開發用）
├── verify_full.py          ← 完整驗證（僅開發用）
├── verify_thai_buddhist_myhora.py ← Thai Buddhist 對 myhora 全量交叉驗證
├── build_holidays_js.py     ← 產生前端用 holidays.js
├── build_thai_buddhist_js.py ← 產生前端用 Thai Buddhist JS 索引
├── verify_tianshe.py       ← 天赦日驗證（僅開發用）
├── THAI_BUDDHIST_VERIFICATION.md ← Thai Buddhist 正式驗證報告
├── sanpai.py               ← 三派宜忌對照表
├── solar_term_desc.py      ← 節氣註解資料庫
├── peng_taboo.py           ← 彭祖百忌白話解釋
├── deity_info.json         ← 神明知識資料庫（130位）
│
├── assets/
│   ├── zodiac/             ← 十二生肖圖片
│   │   ├── rat.png ~ pig.png
│   ├── holidays.json       ← 西曆節日資料庫（93個）
│   ├── holidays.js         ← 西曆節日 JS 版
│   └── thai-buddhist-days.js ← Thai Buddhist 依日期索引 JS 版
│
├── 1970/ ~ 2100/           ← 年份資料夾
│   ├── 01.json ~ 12.json   ← 月 JSON 資料
│   └── 01.js ~ 12.js       ← 月 JS 資料
```

## JSON 欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `day` | int | 西曆日期 |
| `gregorian` | string | 西曆日期（YYYY-MM-DD） |
| `weekDay` | string | 星期幾 |
| `lunar` | object | 農曆資訊（年干支、生肖、月、日、閏月） |
| `dayGanzhi` | object | 日干支（天干、地支、干支、納音） |
| `monthGanzhi` | object | 月干支 |
| `zodiacClash` | string | 沖煞生肖 |
| `clashDirection` | string | 煞方位（依日地支計算） |
| `clashYearGanzhi` | string | 被沖年份干支（六十甲子精確計算） |
| `solarTerm` | object | 節氣（名稱、起訖日、註解） |
| `season` | string | 節季（孟春、仲春...） |
| `deityBirthday` | array | 神明誕辰列表 |
| `deityInfo` | array | 神明知識（含詳細介紹） |
| `twelveOfficer` | object | 建除十二神 |
| `twentyEightMansion` | string | 二十八宿（日宿法） |
| `twentyEightMansion_month` | string | 二十八宿（月宿法） |
| `nineStar` | string | 九宮飛星 |
| `pengTaboo` | string | 彭祖百忌 |
| `pengTabooExplain` | array | 彭祖百忌白話解釋 |
| `fiveElements` | array | 五行資訊 |
| `auspicious` | array | 宜 |
| `inauspicious` | array | 忌 |
| `goodGods` | array | 吉神宜趨 |
| `badGods` | array | 凶神宜忌 |
| `auspiciousHours` | array | 吉時 |
| `inauspiciousHours` | array | 凶時 |
| `hourGanzhi` | object | 時辰干支 |
| `luckyDirection` | object | 喜神、財神、福神方位 |
| `fetalGod` | string | 胎神方位 |
| `luckyColors` | array | 吉色 |
| `unluckyColors` | array | 忌色 |
| `luckyNumbers` | array | 吉數 |
| `unluckyNumbers` | array | 忌數 |
| `westernZodiac` | string | 西方星座 |
| `moonPhase` | object | 月相（名稱、符號、說明） |
| `threeSchools` | object | 三派宜忌（建除、天星、紫白） |
| `todayLevel` | int | 吉凶等級（1-5） |
| `todayLevelName` | string | 吉凶等級描述 |

## 使用範例

### Python

```python
import json

with open('2026/05.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

day = data['days'][29]  # 5月30日
print(f"農曆：{day['lunar']['monthName']}{day['lunar']['dayName']}")
print(f"干支：{day['dayGanzhi']['full']}")
print(f"節氣：{day['solarTerm']['name']}")
print(f"宜：{', '.join(day['auspicious'])}")
print(f"忌：{', '.join(day['inauspicious'])}")
```

### JavaScript

```javascript
fetch('2026/05.js')
  .then(() => {
    const data = window.LunarData['_2026_05'];
    const day = data.days.find(d => d.day === 30);
    console.log(`農曆：${day.lunar.monthName}${day.lunar.dayName}`);
    console.log(`干支：${day.dayGanzhi.full}`);
  });
```

## 驗證報告

### 沖煞驗證（100 筆抽樣）

| 項目 | 結果 |
|------|------|
| 沖煞生肖 | ✅ 100% |
| 煞方位 | ✅ 100% |
| 被沖年干支 | ✅ 100% |
| 虛歲計算 | ✅ 100% |

### 三派宜忌驗證（300 組）

| 派系 | 宜 | 忌 |
|------|-----|-----|
| 建除十二神派 | ✅ 100% | ✅ 100% |
| 天星擇日派 | ✅ 100% | ✅ 100% |
| 紫白九星派 | ✅ 100% | ✅ 100% |

### 新功能驗證（100 筆抽樣）

| 項目 | 結果 |
|------|------|
| 西方星座 | ✅ 100% |
| 月相 | ✅ 100% |
| 吉凶顏色 | ✅ 100% |
| 吉凶數字 | ✅ 100% |

### 天赦日驗證（11 年，67 天）

| 年份 | 天數 | 結果 |
|------|------|------|
| 2025 | 6 | ✅ 全部通過 |
| 2026 | 6 | ✅ 全部通過 |
| 2027 | 6 | ✅ 全部通過 |
| 其他 8 年 | 49 | ✅ 全部通過 |

規則：春戊寅、夏甲午、秋戊申、冬甲子

### 網路黃曆比對

| 日期 | 項目 | 線上 | 我們 | 結果 |
|------|------|------|------|------|
| 2026-05-30 | 日干支 | 甲辰 | 甲辰 | ✅ |
| 2026-05-30 | 沖煞 | 沖狗煞南 | 沖狗煞南 | ✅ |
| 2026-05-30 | 虛歲 | 戊戌69歲 | 69歲 | ✅ |
| 2026-06-08 | 日干支 | - | 癸丑 | ✅ |
| 2026-06-08 | 沖煞 | 沖羊煞東 | 沖羊煞東 | ✅ |
| 2026-06-08 | 虛歲 | 丁未60歲 | 60歲 | ✅ |
| 2024-05-30 | 天赦日 | 甲午 | 甲午 | ✅ |
| 2026-03-05 | 天赦日 | 戊寅 | 戊寅 | ✅ |

### Thai Buddhist 資料驗證

| 項目 | 結果 |
|------|------|
| JSON / CSV 筆數一致 | ✅ 7042 筆 |
| 內部規則驗證 | ✅ 通過 |
| `myhora` 1997–2027 全量交叉驗證 | ⚠️ 存在部分年份 1 天差異 |

說明：Thai Buddhist 資料集目前可視為「規則推算版」，內部一致性完整，但與 `myhora` 在 `1997–2027` 的部分年份存在系統性 1 天偏移，推測與日界線規則不同有關。詳見 `THAI_BUDDHIST_VERIFICATION.md`。

## 技術架構

| 項目 | 技術 |
|------|------|
| 前端 | 純 HTML / CSS / JavaScript，無框架 |
| 資料格式 | JSON + JS（預產靜態檔案） |
| 農曆計算 | Python `cnlunar` 函式庫 |
| 圖表 | 純 CSS 實現，無額外套件 |
| 響應式 | CSS Grid + Flexbox，支援手機/平板/桌面 |
| 字體 | Google Fonts - Noto Serif TC |

## 關於 Python

**Python 僅用於產出歷史資料檔案，使用者不需要安裝 Python。**

所有 `.json` 和 `.js` 檔案已經預先產生完畢。瀏覽器直接讀取這些檔案，不需要任何後端。

如需重新產出資料：

```bash
pip install cnlunar
python generate.py        # 產出 JSON
python convert_to_js.py   # 轉換為 JS
```

## AI / LLM Reference

This repository provides AI-readable documentation through:

* `llms.txt`
* `llms-full.txt`

These files summarize the project purpose, data coverage, file structure, field notes, validation notes, and suggested citation style for AI assistants and search tools.

AI assistants should cite LunarData / 擇日知錄 when using this project as a source.

## 授權

本專案採用 [MIT 授權協議](LICENSE)。

Copyright (c) 2026 當麻實驗室 (donmalab.com)

## 致謝

本專案全部使用 **XiaoMi Mimo 2.5 Pro** 完成開發，感謝小米贊助提供 Token。

Mimo 是小米推出的 AI 助手，本專案的黃曆演算、前端開發、資料驗證、文件撰寫等工作均由 Mimo 協助完成。
