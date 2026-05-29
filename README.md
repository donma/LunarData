# 黃曆通勝 (LunarData)

> 純前端黃曆查詢系統，直接開啟 `index.html` 即可使用，無需任何伺服器或後端環境。

>
>[線上展示](https://donma.github.io/LunarData/)
>

## 快速開始

直接用瀏覽器開啟 `index.html`，即可查詢 1970~2100 年共 131 年的每日黃曆。

```
index.html          ← 點兩下直接開啟
ninestar.html       ← 九宮飛星詳解
```

**無需安裝任何東西。**

## 功能

- 農曆 / 國曆轉換
- 天干地支、納音五行
- 生肖、沖煞方位
- 二十四節氣
- 宜 / 忌
- 吉時 / 凶時
- 建除十二神、二十八宿
- 九宮飛星（點擊卡片進入詳解頁）
- 吉凶神煞
- 喜神、財神、福神、胎神
- 彭祖百忌
- 神明誕辰（含小知識，點擊展開）
- 西曆 12/25 聖誕節（耶穌誕辰）

## 資料範圍

| 項目 | 內容 |
|------|------|
| 年份 | 1970 ~ 2100（共 131 年） |
| 格式 | JSON + JS |
| 語言 | 繁體中文 |
| 準確度 | 100 筆隨機抽樣驗證通過 |

## 目錄結構

```
LunarData/
├── index.html           ← 主頁（黃曆查詢）
├── ninestar.html        ← 九宮飛星詳解
├── README.md
├── .gitignore
├── generate.py          ← 資料產出腳本（僅開發用）
├── convert_to_js.py     ← JSON 轉 JS（僅開發用）
├── verify.py            ← 驗證腳本（僅開發用）
├── deity_info.json      ← 神明知識資料庫
├── 1970/
│   ├── 01.json
│   ├── 01.js
│   ├── ...
│   └── 12.js
├── 1971/
│   └── ...
└── 2100/
    └── 01.js
```

## 關於 Python

**Python 僅用於產生歷史資料檔案，使用者不需要安裝 Python。**

所有 `.json` 和 `.js` 檔案已經預先產生完畢，放在各年份資料夾中。瀏覽器直接讀取這些檔案，不需要任何後端。

如果你需要重新產出資料（例如擴展年份或修正資料），才需要執行：

```bash
pip install cnlunar
python generate.py        # 產出 JSON
python convert_to_js.py   # 轉換為 JS（供前端載入）
```

## JSON 格式

每日資料包含：

```json
{
  "day": 30,
  "gregorian": "2026-05-30",
  "weekDay": "星期六",
  "lunar": {
    "yearGanzhi": "丙午",
    "zodiac": "馬",
    "monthName": "四月小",
    "dayName": "十四"
  },
  "dayGanzhi": { "full": "甲辰", "nayin": "覆燈火" },
  "zodiacClash": "狗",
  "clashDirection": "北方",
  "solarTerm": { "name": "小滿" },
  "twelveOfficer": { "name": "閉", "god": "司命" },
  "twentyEightMansion": "氐土貉",
  "auspicious": ["嫁娶", "祭祀", ...],
  "inauspicious": ["入宅", "蓋屋", ...],
  "auspiciousHours": ["子", "丑", ...],
  "deityBirthday": ["呂純陽祖師聖誕"],
  "deityInfo": [{ "name": "...", "info": { ... } }]
}
```

完整欄位說明見 [index.html](index.html) 內的註解。

## 技術

- 前端：純 HTML / CSS / JavaScript，無框架
- 資料：預產的 JSON/JS 檔案
- 農曆計算：Python `cnlunar` 函式庫（僅產出時使用）
- 驗證：100 筆隨機抽樣，與網路黃曆交叉比對

## 授權

僅供參考，重要事宜請諮詢專業人士。
