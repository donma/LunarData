# 擇日知錄 - 農民曆

> 整合農曆、干支、節氣、宜忌、吉時、神明誕辰、彭祖百忌、九宮飛星與多種傳統曆法資訊，純前端即可查詢。
>
> 「我願稱之目前地表最強農民曆」
>
> 線上展示：**https://donma.github.io/LunarData/**

## 功能特色

### 黃曆核心
- 農曆 / 國曆轉換
- 天干地支（年柱、月柱、日柱）
- 生肖、沖煞方位、虛歲
- 二十四節氣（含白話註解）
- 宜 / 忌（含白話解釋 tooltip）
- 吉時 / 凶時（含時辰干支）
- 建除十二神
- 二十八宿（日宿法 + 月宿法雙算法）
- 九宮飛星
- 彭祖百忌（含幽默白話文解釋，如「甲日別亂開錢包借錢給人，否則錢財跟你說掰掰」）
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

### 特色節日
- **天穿日**（農曆正月二十）— 客家傳統節日，女媧補天紀念日
- **天赦日**（春戊寅、夏甲午、秋戊申、冬甲子）— 百無禁忌的黃道吉日
- **冷門國際節日** — 93 個西曆節日，包含國際壽司日、海盜說話日、醜毛衣日等趣味節日
- **農曆傳統節日** — 春節、端午、中秋、重陽、除夕等 12 個重要節日

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
├── .gitignore
│
├── generate.py             ← 資料產出腳本（僅開發用）
├── convert_to_js.py        ← JSON 轉 JS（僅開發用）
├── verify_100.py           ← 100天抽樣驗證（僅開發用）
├── verify_300.py           ← 三派宜忌驗證（僅開發用）
├── verify_new.py           ← 新功能驗證（僅開發用）
├── verify_full.py          ← 完整驗證（僅開發用）
├── sanpai.py               ← 三派宜忌對照表
├── solar_term_desc.py      ← 節氣註解資料庫
├── deity_info.json         ← 神明知識資料庫（130位）
│
├── assets/
│   └── zodiac/             ← 十二生肖圖片
│       ├── rat.png         ← 鼠
│       ├── ox.png          ← 牛
│       ├── tiger.png       ← 虎
│       ├── rabbit.png      ← 兔
│       ├── dragon.png      ← 龍
│       ├── snake.png       ← 蛇
│       ├── horse.png       ← 馬
│       ├── sheep.png       ← 羊
│       ├── monkey.png      ← 猴
│       ├── rooster.png     ← 雞
│       ├── dog.png         ← 狗
│       └── pig.png         ← 豬
│
├── 1970/                   ← 年份資料夾
│   ├── 01.json             ← 1月 JSON 資料
│   ├── 01.js               ← 1月 JS 資料（供前端載入）
│   ├── ...
│   └── 12.js
├── 1971/
│   └── ...
└── 2100/
    └── 01.js
```

## JSON 欄位說明

每日資料包含以下欄位：

| 欄位 | 類型 | 說明 |
|------|------|------|
| `day` | int | 西曆日期 |
| `gregorian` | string | 西曆日期（YYYY-MM-DD） |
| `weekDay` | string | 星期幾 |
| `lunar` | object | 農曆資訊（年干支、生肖、月、日、閏月） |
| `dayGanzhi` | object | 日干支（天干、地支、干支、納音） |
| `monthGanzhi` | object | 月干支 |
| `zodiacClash` | string | 沖煞生肖 |
| `clashDirection` | string | 煞方位 |
| `clashYearGanzhi` | string | 被沖年份干支 |
| `solarTerm` | object | 節氣（名稱、起訖日、註解） |
| `season` | string | 節季（孟春、仲春...） |
| `deityBirthday` | array | 神明誕辰列表 |
| `deityInfo` | array | 神明知識（含詳細介紹） |
| `twelveOfficer` | object | 建除十二神 |
| `twentyEightMansion` | string | 二十八宿（日宿法） |
| `twentyEightMansion_month` | string | 二十八宿（月宿法） |
| `nineStar` | string | 九宮飛星 |
| `pengTaboo` | string | 彭祖百忌 |
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

## 技術架構

| 項目 | 技術 |
|------|------|
| 前端 | 純 HTML / CSS / JavaScript，無框架 |
| 資料格式 | JSON + JS（預產靜態檔案） |
| 農曆計算 | Python `cnlunar` 函式庫 |
| 圖表 | 純 CSS 實現，無額外套件 |
| 響應式 | CSS Grid + Flexbox，支援手機/平板/桌面 |

## 驗證報告

### 沖煞驗證（100筆抽樣）

| 項目 | 結果 |
|------|------|
| 沖煞生肖 | ✅ 100% |
| 煞方位 | ✅ 100% |
| 被沖年干支 | ✅ 100% |
| 虛歲計算 | ✅ 100% |

### 三派宜忌驗證（300組）

| 派系 | 宜 | 忌 |
|------|-----|-----|
| 建除十二神派 | ✅ 100% | ✅ 100% |
| 天星擇日派 | ✅ 100% | ✅ 100% |
| 紫白九星派 | ✅ 100% | ✅ 100% |

### 新功能驗證（100筆抽樣）

| 項目 | 結果 |
|------|------|
| 西方星座 | ✅ 100% |
| 月相 | ✅ 100% |
| 吉凶顏色 | ✅ 100% |
| 吉凶數字 | ✅ 100% |

## 關於 Python

**Python 僅用於產出歷史資料檔案，使用者不需要安裝 Python。**

所有 `.json` 和 `.js` 檔案已經預先產生完畢。瀏覽器直接讀取這些檔案，不需要任何後端。

如需重新產出資料：

```bash
pip install cnlunar
python generate.py        # 產出 JSON
python convert_to_js.py   # 轉換為 JS
```

## 授權

本專案採用 [MIT 授權協議](LICENSE)。

```
MIT License

Copyright (c) 2026 當麻實驗室

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 致謝

本專案全部使用 **XiaoMi Mimo 2.5 Pro** 完成開發，感謝小米贊助提供 Token。

Mimo 是小米推出的 AI 助手，本專案的黃曆演算、前端開發、資料驗證、文件撰寫等工作均由 Mimo 協助完成。
