# Thai Buddhist 資料驗證報告

## 結論

`thai-buddhist-days-1970-2100.json` / `.csv` 可以視為一份 **內部規則一致、結構完整** 的 Thai Buddhist 事件資料集，但目前**不建議直接當成最終權威版併入農民曆主資料**，原因是它與可取得的外部年表來源 `myhora` 在 `1997–2027` 區間仍有系統性 1 天差異。

比較保守的建議是：

1. 先不要把它混入主黃曆核心欄位，避免把未完全定案的日期當成既定正解。
2. 若要先收錄，請明確標示為「泰國佛日參考資料（規則推算版）」。
3. 後續若要正式納入，應先統一採用哪一種日界線規則，再重做全量產生與比對。

## 驗證範圍

- 檔案：`thai-buddhist-days-1970-2100.json`
- 檔案：`thai-buddhist-days-1970-2100.csv`
- 事件類型：`wan_phra`、`sao_ha_candidate`、`makha_bucha`、`visakha_bucha`、`khao_phansa`、`ok_phansa`
- 內部全量驗證範圍：`1970-01-01` ~ `2100-12-31`
- 外部交叉驗證範圍：`1997` ~ `2027`（`myhora` 可取得完整年表區間）

## 內部全量驗證結果

已完成的全量內部驗證結果如下：

- `metadata.recordCount = 7042`
- JSON `events` 筆數 = `7042`
- CSV 筆數 = `7042`
- JSON / CSV 完全一致
- `duplicate_date_event_pairs = 0`
- `out_of_range = 0`
- `sorted_non_decreasing = True`
- `weekday_mismatches = 0`
- `be_year_mismatches = 0`
- `category_mismatches = 0`
- `wan_phra_rule_violations = 0`
- `major_rule_violations = 0`
- `year_count_anomalies = 0`
- `sao_ha_rule_violations = 0`
- `khao_prev_fullmoon8_matches = True`

這表示資料集本身沒有明顯結構錯誤、排序錯誤、重複資料或規則自相矛盾問題。

## 外部交叉驗證方法

新增腳本：`verify_thai_buddhist_myhora.py`

用途：

- 逐年抓取 `myhora` 的 Buddhist 年表頁面
- 解析全年 `wan_phra`
- 解析四個主要佛教節日：`makha_bucha`、`visakha_bucha`、`khao_phansa`、`ok_phansa`
- 與本地 `thai-buddhist-days-1970-2100.json` 在 `1997–2027` 做全量逐日比對

執行方式：

```powershell
& "C:\Users\no2so\AppData\Local\Programs\Python\Python312\python.exe" "D:\AI_PROJECTS\LunarData\verify_thai_buddhist_myhora.py"
```

## 外部交叉驗證結果

`myhora` 抓取 31 個年份全部成功：

- `fetch_errors = 0`
- `total_parsed_rows = 1565`

比對總結：

- `compared_local_event_records = 1658`
- `total_mismatched_dates = 590`
- `overall_match = MISMATCH`

各事件結果：

| eventId | local_count | myhora_count | missing_count | extra_count | 結果 |
|---|---:|---:|---:|---:|---|
| `wan_phra` | 1534 | 1534 | 273 | 273 | 不一致 |
| `makha_bucha` | 31 | 31 | 6 | 6 | 不一致 |
| `visakha_bucha` | 31 | 31 | 6 | 6 | 不一致 |
| `khao_phansa` | 31 | 31 | 5 | 5 | 不一致 |
| `ok_phansa` | 31 | 31 | 5 | 5 | 不一致 |

## 差異模式

差異不是隨機散落，而是集中在以下年份出現 **整批事件晚 1 天** 的現象：

- `1997`
- `1998`
- `1999`
- `2000`
- `2005`
- `2006`
- `2014`
- `2015`
- `2016`

主要佛教節日的差異全部都是：

- 本地資料日期 = `myhora` 日期 `+1` 天

例如：

| 事件 | 本地資料 | myhora |
|---|---|---|
| `makha_bucha` | `1997-02-22` | `1997-02-21` |
| `visakha_bucha` | `1997-05-21` | `1997-05-20` |
| `khao_phansa` | `1998-07-10` | `1998-07-09` |
| `ok_phansa` | `1998-10-06` | `1998-10-05` |
| `khao_phansa` | `2015-08-01` | `2015-07-31` |

`wan_phra` 也是同類型現象。受影響年份中，有些年份是全年全部晚 1 天，有些年份是年內一段期間晚 1 天、另一段期間又對齊，因此腳本輸出會看到 `delta_days=[1]` 或 `delta_days=[0,1]`。

## 最可能原因

`myhora` 年表頁面明確寫出：

> รอบวันทางจันทรคติไทย นับตามเวลาดวงอาทิตย์ขึ้นจริง หรือประมาณ เวลา 06:00น. ถึง 05:59น. (วันรุ่งขึ้น)

也就是它採的是 **接近日出換日** 的 Thai lunar day 邏輯，而不是單純以公曆 `00:00–23:59` 當作日期切換。

目前這份資料集的 metadata 只寫：

- `timezone = Asia/Bangkok`
- `calendar = Thai lunisolar calendar via pythaidate CsDate`

但沒有額外標明是否採用與 `myhora` 相同的「日出換日」規則。從交叉驗證結果看，差異高度像是：

- 本地資料以一般 civil date 取值
- `myhora` 以 Thai lunar day 的日界線取值

因此，現階段最合理的定性不是「資料亂算」，而是：

- **規則系統內部一致**
- 但與外部來源使用的日界線規則未對齊

## 可驗證與不可驗證區段

目前能做到的最嚴格外部驗證範圍：

- `1997–2027`：可用 `myhora` 做全年完整交叉驗證

目前無法做到同等級外部全量驗證的範圍：

- `1970–1996`
- `2028–2100`

原因：

- 尚未找到覆蓋 `1970–2100` 全時段、可穩定抓取、可機器比對的第二套公開年表來源
- `timeanddate.com` 會遇到 Cloudflare / `403`
- `publicholidays.asia`、`worlddata.info` 覆蓋年限太短
- `jhanarato/uposatha` 只覆蓋近年區間

## 對納入農民曆的建議

### 不建議的做法

- 直接把目前資料無註記地混入主黃曆，並宣稱是外部完全驗證後的正式結果

### 可接受的做法

1. 以獨立模組收錄，標示為「規則推算版」
2. 在 UI 或 README 註明：與部分泰國年表來源可能存在 1 天日界線差異
3. 待日界線規則定案後，再重產一次資料並重做 `1997–2027` 全量比對

### 若要升級為正式主資料

至少還需要完成：

1. 明確定義採用 `00:00` 換日，或採用 Thai lunar day / 日出換日
2. 依該規則重產 `1970–2100` 全量資料
3. 再跑一次 `myhora 1997–2027` 全量交叉驗證
4. 若可能，再補第二套獨立來源做近年交叉驗證

## 目前新增檔案

- `verify_thai_buddhist_myhora.py`：`myhora 1997–2027` 全量外部交叉驗證腳本
- `THAI_BUDDHIST_VERIFICATION.md`：本報告
