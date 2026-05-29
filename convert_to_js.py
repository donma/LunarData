# -*- coding: utf-8 -*-
"""
將 JSON 檔案轉換為可被 <script> 標籤載入的 JS 檔案
"""

import sys
import io
if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os

def convert_json_to_js(base_dir):
    """將所有 JSON 轉為 JS"""
    count = 0
    for year_dir in sorted(os.listdir(base_dir)):
        if not year_dir.isdigit():
            continue
        year_path = os.path.join(base_dir, year_dir)
        if not os.path.isdir(year_path):
            continue

        for filename in sorted(os.listdir(year_path)):
            if not filename.endswith('.json'):
                continue

            json_path = os.path.join(year_path, filename)
            js_path = json_path.replace('.json', '.js')

            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            month_key = f"_{year_dir}_{filename.replace('.json', '')}"
            js_content = f"window.LunarData['{month_key}'] = {json.dumps(data, ensure_ascii=False)};"

            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js_content)

            count += 1

    print(f"已轉換 {count} 個檔案")

if __name__ == "__main__":
    base_dir = r"D:\AI_PROJECTS\LunarData"
    convert_json_to_js(base_dir)
