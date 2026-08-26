# 擇日知錄 - 農民曆
# LunarData

> 整合農曆、干支、節氣、宜忌、吉時、神明誕辰、彭祖百忌、二十八宿、九宮飛星與多種傳統曆法資訊。
>
> **我願稱之目前地表最強農民曆。**

**[線上展示](https://donma.github.io/LunarData/)**

LunarData 不只是一個農民曆網站。

這個專案將 **1970–2100 共 131 年、約 47,847 天** 的傳統曆法資訊整理成結構化資料，提供 JSON 與 JavaScript 格式。

你可以直接把它當農民曆使用，也可以拿來做：

- 民俗與曆法研究
- 資料分析
- AI / RAG Dataset
- 日期 API
- App / Web / Bot
- 資料視覺化
- 傳統文化研究

---

## 收錄內容

### 黃曆核心

- 農曆 / 國曆
- 年、月、日干支
- 十二生肖
- 沖煞與方位
- 二十四節氣
- 宜 / 忌
- 吉時 / 凶時
- 建除十二神
- 二十八宿
- 九宮飛星
- 彭祖百忌
- 五行
- 喜神 / 財神 / 福神
- 胎神方位

### 民俗與文化

- 神明誕辰與介紹
- 傳統農曆節日
- 天穿日
- 天赦日
- 西方星座
- 月相
- 冷門國際節日

### 三派擇日

同時整理三套不同擇日觀點：

- 建除十二神派
- 天星擇日派
- 紫白九星派

方便查詢，也適合做不同傳統系統之間的比較研究。

---

## 資料範圍

| 項目 | 內容 |
|---|---|
| 年份 | 1970–2100 |
| 年數 | 131 年 |
| 每日資料 | 約 47,847 天 |
| 格式 | JSON + JavaScript |
| 語言 | 繁體中文 |
| 使用方式 | 可完全離線 |
| License | MIT |

資料依年份與月份存放：

```text
2026/
├── 01.json
├── 01.js
├── 02.json
├── 02.js
└── ...
```

例如：

```text
2026/05.json
```

就是 2026 年 5 月完整資料。

---

## 每一天包含什麼？

一筆每日資料不只是農曆日期。

還可能包含：

```text
西曆日期
農曆日期
星期

年干支
月干支
日干支
納音

生肖
沖煞
煞方

節氣
節季

神明誕辰
神明介紹

十二建除
二十八宿
九宮飛星

彭祖百忌
五行

宜
忌
吉神
凶神

吉時
凶時
時辰干支

喜神方位
財神方位
福神方位
胎神方位

吉色
忌色
吉數
忌數

西方星座
月相

三派擇日結果
```

因此 LunarData 不只是畫面上的農民曆，也是一套可以直接分析的 **Traditional Chinese Calendar Dataset**。

---

## 給一般使用者

直接打開：

```text
index.html
```

即可使用。

不需要：

```text
Node.js
Database
Docker
API Key
Backend Server
```

整套系統可以純前端執行。

---

## 給資料研究者

如果你只需要資料，可以直接使用：

```text
1970/
1971/
1972/
...
2100/
```

每個月份都有 JSON。

適合匯入：

- Pandas
- R
- SQLite
- DuckDB
- Power BI
- Tableau
- AI / LLM
- RAG

可以研究例如：

- 干支循環
- 五行分布
- 節氣變化
- 二十八宿
- 神明誕辰分布
- 宜忌出現頻率
- 不同擇日派別差異

---

## JavaScript 使用

每個月份同時提供 `.js` 版本。

```html
<script src="2026/05.js"></script>
```

```javascript
const data = window.LunarData["_2026_05"];

const day = data.days.find(x => x.day === 30);

console.log(day.lunar);
console.log(day.dayGanzhi);
console.log(day.auspicious);
console.log(day.inauspicious);
```

因此不需要另外建立 API Server。

---

## 九宮飛星

專案另外提供：

```text
ninestar.html
```

包含：

- 洛書九宮圖
- 九星飛行順序
- 五行相生相剋
- 三元九運
- 各星宜忌說明

---

## 泰國佛教日期資料

另外整理部分 Thai Buddhist 日期資料，包括：

- Wan Phra
- Makha Bucha
- Visakha Bucha
- Khao Phansa
- Ok Phansa

這部分目前標示為 **規則推算參考資料**。

由於泰國傳統 lunar day 日界線與一般午夜換日方式可能不同，因此專案另外保留完整交叉驗證報告：

```text
THAI_BUDDHIST_VERIFICATION.md
```

不確定的資料，不硬宣稱是唯一正解。

---

## 資料驗證

專案內保留多套驗證腳本，包括：

- 干支
- 沖煞
- 煞方
- 六十甲子
- 建除十二神
- 三派宜忌
- 月相
- 西方星座
- 天赦日
- Thai Buddhist 外部資料比對

LunarData 的原則不是宣稱所有傳統曆法只有唯一算法。

而是：

**能計算的留下算法，能驗證的留下驗證，有差異的地方就把差異留下來。**

---

## 專案定位

LunarData 可以是一個：

**農民曆**

也可以是一個：

**Traditional Chinese Calendar Dataset**

更可以是一套拿來研究：

```text
曆法
時間
天文
民俗
宗教
文化
傳統週期
```

的開放資料。

---

## License

MIT License

歡迎自由使用、研究、修改與二次開發。

如果這個專案對你有幫助，歡迎 Star。

---

**LunarData**

**1970–2100 / 131 Years / ~47,847 Days**

把傳統農民曆，整理成可以被人閱讀，也可以被電腦研究的資料。

## 授權

本專案採用 [MIT 授權協議](LICENSE)。

Copyright (c) 2026 當麻實驗室 (donmalab.com)

## 致謝

本專案全部使用 **XiaoMi Mimo 2.5 Pro** 完成開發，感謝小米贊助提供 Token。

Mimo 是小米推出的 AI 助手，本專案的黃曆演算、前端開發、資料驗證、文件撰寫等工作均由 Mimo 協助完成。
