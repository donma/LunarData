# -*- coding: utf-8 -*-
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "assets" / "holidays.json"
TARGET_PATH = BASE_DIR / "assets" / "holidays.js"


def main():
    data = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    TARGET_PATH.write_text(
        f"window.HolidaysData = {json.dumps(data, ensure_ascii=False)}\n",
        encoding="utf-8",
    )
    print(f"Wrote {TARGET_PATH}")


if __name__ == "__main__":
    main()
