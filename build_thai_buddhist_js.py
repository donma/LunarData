# -*- coding: utf-8 -*-
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "thai-buddhist-days-1970-2100.json"
TARGET_PATH = BASE_DIR / "assets" / "thai-buddhist-days.js"


def main():
    payload = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    grouped = {}

    for event in payload["events"]:
        date_str = event["date"]
        grouped.setdefault(date_str, []).append(
            {
                "eventId": event["eventId"],
                "nameZh": event["nameZh"],
                "nameThai": event["nameThai"],
                "nameEn": event["nameEn"],
                "category": event["category"],
                "buddhistEraYear": event["buddhistEraYear"],
                "weekdayZh": event["weekdayZh"],
                "thaiLunarText": event["thaiLunar"]["text"],
                "thaiLunarMonth": event["thaiLunar"]["month"],
                "thaiLunarHalf": event["thaiLunar"]["half"],
                "thaiLunarDayInHalf": event["thaiLunar"]["dayInHalf"],
                "note": event.get("note", ""),
            }
        )

    serialized = json.dumps(grouped, ensure_ascii=False, separators=(",", ":"))
    TARGET_PATH.write_text(f"window.ThaiBuddhistDataByDate={serialized};\n", encoding="utf-8")
    print(f"Wrote {TARGET_PATH}")


if __name__ == "__main__":
    main()
