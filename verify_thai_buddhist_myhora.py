# -*- coding: utf-8 -*-
import html
import json
import re
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "thai-buddhist-days-1970-2100.json"
START_YEAR = 1997
END_YEAR = 2027
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

THAI_MONTHS = {
    "มกราคม": 1,
    "กุมภาพันธ์": 2,
    "มีนาคม": 3,
    "เมษายน": 4,
    "พฤษภาคม": 5,
    "มิถุนายน": 6,
    "กรกฎาคม": 7,
    "สิงหาคม": 8,
    "กันยายน": 9,
    "ตุลาคม": 10,
    "พฤศจิกายน": 11,
    "ธันวาคม": 12,
}

THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")

TARGET_EVENT_IDS = {
    "wan_phra",
    "makha_bucha",
    "visakha_bucha",
    "khao_phansa",
    "ok_phansa",
}

REMARK_TO_EVENT_ID = {
    "วันมาฆบูชา": "makha_bucha",
    "วันวิสาขบูชา": "visakha_bucha",
    "วันเข้าพรรษา": "khao_phansa",
    "วันออกพรรษา": "ok_phansa",
}

ROW_RE = re.compile(
    r"<div class=['\"]holi bud-day['\"]>"
    r"\s*<div class=['\"]bud-d7['\"]>(?P<weekday>.*?)</div>"
    r"\s*<div class=['\"]bud-d['\"]>(?P<day>\d{1,2})</div>"
    r"\s*<div class=['\"]bud-mm['\"]>(?P<month>.*?)</div>"
    r"\s*<div class=['\"]bud-yy['\"]>(?P<year>\d{4})</div>"
    r"\s*<div class=['\"]bud-luday['\"]>(?P<lunar>.*?)</div>"
    r"\s*<div class=['\"]bud-rem['\"]>(?P<remark>.*?)</div>"
    r"\s*</div><!--myhora\.com-->",
    re.S,
)


def clean_html_text(value):
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_lunar_text(value):
    return clean_html_text(value).translate(THAI_DIGITS)


def is_wan_phra_lunar(value):
    normalized = normalize_lunar_text(value)
    prefixes = (
        "ขึ้น 8 ค่ำ",
        "ขึ้น 15 ค่ำ",
        "แรม 8 ค่ำ",
        "แรม 14 ค่ำ",
        "แรม 15 ค่ำ",
    )
    return normalized.startswith(prefixes)


def fetch_year_page(year):
    buddhist_era_year = year + 543
    url = f"https://myhora.com/calendar/buddhist-{buddhist_era_year}.aspx"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def parse_myhora_year(year, html_text):
    parsed = defaultdict(set)
    row_count = 0

    for match in ROW_RE.finditer(html_text):
        row_count += 1
        day = int(match.group("day"))
        month_name = clean_html_text(match.group("month"))
        month = THAI_MONTHS.get(month_name)
        if month is None:
            raise ValueError(f"{year}: unknown Thai month name: {month_name}")

        row_year = int(match.group("year")) - 543
        if row_year != year:
            raise ValueError(f"{year}: unexpected row year {row_year}")

        date_str = f"{year:04d}-{month:02d}-{day:02d}"
        lunar_text = match.group("lunar")
        remark_text = clean_html_text(match.group("remark"))

        if is_wan_phra_lunar(lunar_text):
            parsed["wan_phra"].add(date_str)

        for thai_name, event_id in REMARK_TO_EVENT_ID.items():
            if thai_name in remark_text:
                parsed[event_id].add(date_str)

    return parsed, row_count


def load_local_events():
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    by_event = defaultdict(set)

    for event in payload["events"]:
        year = event["gregorianYear"]
        event_id = event["eventId"]
        if START_YEAR <= year <= END_YEAR and event_id in TARGET_EVENT_IDS:
            by_event[event_id].add(event["date"])

    return payload, by_event


def summarize_differences(local_dates, remote_dates):
    missing = sorted(local_dates - remote_dates)
    extra = sorted(remote_dates - local_dates)
    return {
        "missing": missing,
        "extra": extra,
        "match": not missing and not extra,
    }


def summarize_year_mismatches(local_dates, remote_dates):
    local_by_year = defaultdict(list)
    remote_by_year = defaultdict(list)

    for value in sorted(local_dates):
        local_by_year[int(value[:4])].append(value)
    for value in sorted(remote_dates):
        remote_by_year[int(value[:4])].append(value)

    years = sorted(set(local_by_year) | set(remote_by_year))
    results = []

    for year in years:
        local_year_dates = local_by_year.get(year, [])
        remote_year_dates = remote_by_year.get(year, [])
        if local_year_dates == remote_year_dates:
            continue

        day_deltas = []
        if len(local_year_dates) == len(remote_year_dates):
            for local_value, remote_value in zip(local_year_dates, remote_year_dates):
                day_deltas.append(
                    (date.fromisoformat(local_value) - date.fromisoformat(remote_value)).days
                )

        results.append(
            {
                "year": year,
                "local_count": len(local_year_dates),
                "remote_count": len(remote_year_dates),
                "day_deltas": sorted(set(day_deltas)),
            }
        )

    return results


def main():
    payload, local_by_event = load_local_events()
    remote_by_event = defaultdict(set)
    row_counts = {}
    fetch_errors = {}

    for year in range(START_YEAR, END_YEAR + 1):
        buddhist_era_year = year + 543
        print(f"Fetching myhora {buddhist_era_year}/{year} ...", flush=True)
        try:
            html_text = fetch_year_page(year)
            parsed, row_count = parse_myhora_year(year, html_text)
            row_counts[year] = row_count
            for event_id, dates in parsed.items():
                remote_by_event[event_id].update(dates)
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            fetch_errors[year] = str(exc)

    print()
    print("=" * 72)
    print("Thai Buddhist myhora cross-check (1997-2027)")
    print("=" * 72)
    print(f"local_dataset_records={payload['metadata']['recordCount']}")
    print(f"checked_years={START_YEAR}-{END_YEAR}")
    print(f"checked_year_count={END_YEAR - START_YEAR + 1}")
    print(f"fetch_errors={len(fetch_errors)}")
    print(f"total_parsed_rows={sum(row_counts.values())}")

    if fetch_errors:
        print("fetch_error_details=")
        for year in sorted(fetch_errors):
            print(f"  {year}: {fetch_errors[year]}")

    print()

    overall_ok = not fetch_errors
    compared_total = 0
    mismatch_total = 0

    for event_id in sorted(TARGET_EVENT_IDS):
        local_dates = local_by_event.get(event_id, set())
        remote_dates = remote_by_event.get(event_id, set())
        diff = summarize_differences(local_dates, remote_dates)
        compared_total += len(local_dates)
        mismatch_total += len(diff["missing"]) + len(diff["extra"])
        overall_ok = overall_ok and diff["match"]

        print(f"[{event_id}]")
        print(f"local_count={len(local_dates)}")
        print(f"myhora_count={len(remote_dates)}")
        print(f"missing_count={len(diff['missing'])}")
        print(f"extra_count={len(diff['extra'])}")

        if diff["missing"]:
            print("missing_dates=")
            for date_str in diff["missing"][:20]:
                print(f"  {date_str}")
            if len(diff["missing"]) > 20:
                print(f"  ... {len(diff['missing']) - 20} more")

        if diff["extra"]:
            print("extra_dates=")
            for date_str in diff["extra"][:20]:
                print(f"  {date_str}")
            if len(diff["extra"]) > 20:
                print(f"  ... {len(diff['extra']) - 20} more")

        if diff["match"]:
            print("status=OK")
        else:
            print("status=MISMATCH")
            mismatch_years = summarize_year_mismatches(local_dates, remote_dates)
            print("mismatch_years=")
            for row in mismatch_years:
                delta_text = ",".join(str(delta) for delta in row["day_deltas"]) or "n/a"
                print(
                    f"  {row['year']}: local={row['local_count']} myhora={row['remote_count']} delta_days=[{delta_text}]"
                )
        print()

    print(f"compared_local_event_records={compared_total}")
    print(f"total_mismatched_dates={mismatch_total}")
    print(f"overall_match={'OK' if overall_ok else 'MISMATCH'}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
