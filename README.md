# 黃曆資料庫 (LunarData)

## 概述

本資料庫包含西元 **2026 年至 2099 年**（共 74 年）的每日黃曆資料，以 JSON 格式儲存，全部為**繁體中文**。

## 目錄結構

```
LunarData/
├── README.md           # 本說明文件
├── generate.py         # 資料產出腳本
├── 2026/               # 年份資料夾
│   ├── 01.json         # 1月份資料
│   ├── 02.json         # 2月份資料
│   ├── ...
│   └── 12.json         # 12月份資料
├── 2027/
│   └── ...
└── 2099/
    └── ...
```

## JSON 格式說明

### 月份檔案結構

每個月份檔案（如 `05.json`）包含該月所有天數的黃曆資料：

```json
{
  "year": 2026,
  "month": 5,
  "totalDays": 31,
  "days": [
    { ... },
    { ... },
    ...
  ]
}
```

### 每日資料範例（2026-05-30）

```json
{
  "day": 30,
  "gregorian": "2026-05-30",
  "weekDay": "星期六",
  "lunar": {
    "year": 2026,
    "yearStem": "丙",
    "yearBranch": "午",
    "yearGanzhi": "丙午",
    "zodiac": "馬",
    "month": 4,
    "day": 14,
    "isLeapMonth": false,
    "monthName": "四月小",
    "dayName": "十四"
  },
  "dayGanzhi": {
    "stem": "甲",
    "branch": "辰",
    "full": "甲辰",
    "nayin": "覆燈火"
  },
  "monthGanzhi": {
    "stem": "癸",
    "branch": "巳",
    "full": "癸巳"
  },
  "zodiacClash": "狗",
  "clashDirection": "北方",
  "clashDetail": "龍日沖狗",
  "solarTerm": {
    "name": "小滿",
    "startDate": "2026-05-21",
    "endDate": "2026-06-05",
    "nextName": "芒種",
    "nextDate": "2026-06-05"
  },
  "season": "孟夏",
  "deityBirthday": ["呂純陽祖師聖誕"],
  "twelveOfficer": {
    "name": "閉",
    "god": "司命",
    "isYellowRoad": false
  },
  "twentyEightMansion": "氐土貉",
  "nineStar": "846792351",
  "pengTaboo": "甲不開倉 財物耗散,辰不哭泣 必主重喪",
  "fiveElements": ["天干", "甲", "屬木", "地支", "辰", "屬土", "納音", "火", "屬火"],
  "auspicious": ["諸事不宜"],
  "inauspicious": ["諸事不宜"],
  "goodGods": ["時德", "天官", "天醫", "福生", "月空", "吉慶"],
  "badGods": ["月煞", "月忌", "月虛", "五虛", "荒蕪", "血支"],
  "auspiciousHours": ["寅", "辰", "巳", "申", "酉", "亥"],
  "inauspiciousHours": ["子", "丑", "卯", "午", "未", "戌"],
  "hourGanzhi": {
    "子": "甲子", "丑": "乙丑", "寅": "丙寅", "卯": "丁卯",
    "辰": "戊辰", "巳": "己巳", "午": "庚午", "未": "辛未",
    "申": "壬申", "酉": "癸酉", "戌": "甲戌", "亥": "乙亥"
  },
  "luckyDirection": {
    "喜神": "東北",
    "財神": "東北",
    "福神": "正北",
    "陽貴": "西南",
    "陰貴": "東北"
  },
  "fetalGod": "門雞棲房內東",
  "todayLevel": 4,
  "todayLevelName": "下:凶又逢凶，遇德從忌不從宜，不遇諸事皆忌。",
  "isYellowRoad": false
}
```

## 欄位詳細說明

### 基本資訊

| 欄位 | 類型 | 說明 |
|------|------|------|
| `day` | integer | 西曆日期（日） |
| `gregorian` | string | 西曆日期（YYYY-MM-DD） |
| `weekDay` | string | 星期幾 |

### 農曆資訊 `lunar`

| 欄位 | 類型 | 說明 |
|------|------|------|
| `year` | integer | 農曆年份 |
| `yearStem` | string | 年天干 |
| `yearBranch` | string | 年地支 |
| `yearGanzhi` | string | 年干支（如「丙午」） |
| `zodiac` | string | 生肖 |
| `month` | integer | 農曆月份 |
| `day` | integer | 農曆日期 |
| `isLeapMonth` | boolean | 是否閏月 |
| `monthName` | string | 農曆月名 |
| `dayName` | string | 農曆日名 |

### 日干支 `dayGanzhi`

| 欄位 | 說明 |
|------|------|
| `stem` | 日天干 |
| `branch` | 日地支 |
| `full` | 日干支 |
| `nayin` | 納音五行 |

### 沖煞

| 欄位 | 說明 |
|------|------|
| `zodiacClash` | 沖生肖 |
| `clashDirection` | 沖煞方位 |
| `clashDetail` | 沖煞描述 |

### 節氣 `solarTerm`

| 欄位 | 說明 |
|------|------|
| `name` | 當前節氣 |
| `startDate` | 節氣起始日 |
| `endDate` | 節氣結束日 |
| `nextName` | 下一節氣 |
| `nextDate` | 下一節氣日期 |

### 神明誕辰 `deityBirthday`

陣列，當日神明誕辰名稱。無則為空陣列。

### 建除十二神 `twelveOfficer`

| 欄位 | 說明 |
|------|------|
| `name` | 十二神（建除滿平定執破危成收開閉） |
| `god` | 值日神（青龍明堂天刑朱雀金匱天德白虎玉堂天牢玄武司命勾陳） |
| `isYellowRoad` | 是否黃道日 |

### 二十八宿 `twentyEightMansion`

東方青龍：角木蛟、亢金龍、氐土貉、房日兔、心月狐、尾火虎、箕水豹
北方玄武：斗木獬、牛金牛、女土蝠、虛日鼠、危月燕、室火豬、壁水貐
西方白虎：奎木狼、婁金狗、胃土雉、昴日雞、畢月烏、觜火猴、參水猿
南方朱雀：井木犴、鬼金羊、柳土獐、星日馬、張月鹿、翼火蛇、軫水蚓

### 九星 `nineStar`

| 數字 | 星名 | 五行 |
|------|------|------|
| 1 | 一白貪狼星 | 水 |
| 2 | 二黑巨門星 | 土 |
| 3 | 三碧祿存星 | 木 |
| 4 | 四綠文曲星 | 木 |
| 5 | 五黃廉貞星 | 土 |
| 6 | 六白武曲星 | 金 |
| 7 | 七赤破軍星 | 金 |
| 8 | 八白左輔星 | 土 |
| 9 | 九紫右弼星 | 火 |

### 彭祖百忌 `pengTaboo`

該日天干地支禁忌，如「甲不開倉 財物耗散,辰不哭泣 必主重喪」。

### 宜忌

| 欄位 | 說明 |
|------|------|
| `auspicious` | 宜 |
| `inauspicious` | 忌 |
| `goodGods` | 吉神 |
| `badGods` | 凶神 |

### 時辰

| 欄位 | 說明 |
|------|------|
| `auspiciousHours` | 吉時 |
| `inauspiciousHours` | 凶時 |
| `hourGanzhi` | 時辰干支 |

### 方位 `luckyDirection`

| 欄位 | 說明 |
|------|------|
| `喜神` | 喜神方位 |
| `財神` | 財神方位 |
| `福神` | 福神方位 |
| `陽貴` | 陽貴方位 |
| `陰貴` | 陰貴方位 |

### 胎神 `fetalGod`

當日胎神位置。

### 吉凶等級

| 欄位 | 說明 |
|------|------|
| `todayLevel` | 等級（1最吉～5最凶） |
| `todayLevelName` | 等級描述 |
| `isYellowRoad` | 是否黃道吉日 |

### 節季 `season`

孟春/仲春/季春、孟夏/仲夏/季夏、孟秋/仲秋/季秋、孟冬/仲冬/季冬

## 二十四節氣

| 節氣 | 日期 | 節氣 | 日期 |
|------|------|------|------|
| 立春 | 2/3~2/5 | 立秋 | 8/7~8/9 |
| 雨水 | 2/18~2/20 | 處暑 | 8/22~8/24 |
| 驚蟄 | 3/5~3/7 | 白露 | 9/7~9/9 |
| 春分 | 3/20~3/22 | 秋分 | 9/22~9/24 |
| 清明 | 4/4~4/6 | 寒露 | 10/8~10/9 |
| 穀雨 | 4/19~4/21 | 霜降 | 10/23~10/24 |
| 立夏 | 5/5~5/7 | 立冬 | 11/7~11/8 |
| 小滿 | 5/20~5/22 | 小雪 | 11/22~11/23 |
| 芒種 | 6/5~6/7 | 大雪 | 12/6~12/8 |
| 夏至 | 6/21~6/22 | 冬至 | 12/21~12/23 |
| 小暑 | 7/6~7/8 | 小寒 | 1/5~1/7 |
| 大暑 | 7/22~7/24 | 大寒 | 1/20~1/21 |

## 使用範例

### Python

```python
import json

with open('2026/05.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

day30 = data['days'][29]
print(f"農曆：{day30['lunar']['monthName']}{day30['lunar']['dayName']}")
print(f"干支：{day30['dayGanzhi']['full']}")
print(f"節氣：{day30['solarTerm']['name']}")
print(f"宜：{', '.join(day30['auspicious'])}")
print(f"忌：{', '.join(day30['inauspicious'])}")
```

### JavaScript

```javascript
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('2026/05.json', 'utf-8'));

const day30 = data.days[29];
console.log(`農曆：${day30.lunar.monthName}${day30.lunar.dayName}`);
console.log(`干支：${day30.dayGanzhi.full}`);
console.log(`節氣：${day30.solarTerm.name}`);
```

## 技術說明

- 農曆計算：Python `cnlunar` 函式庫
- 神明誕辰：整理自傳統民俗資料
- 年份範圍：2026-2099（共 74 年），受限於 `cnlunar` 計算範圍

### 重新產出

```bash
python generate.py
```

## 授權

僅供參考，重要事宜請諮詢專業人士。

## 更新紀錄

- 2026-05-30：初始版本，產出 2026-2099 年繁體中文資料
