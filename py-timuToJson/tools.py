import json
import os
import time

# === 设置输入输出文件路径 ===
input_path = "json/danxuan.json"         # ← 替换成你的输入文件
output_path = "updated_output_file.json"    # ← 输出文件

# === 1. 读取 JSON 列表 ===
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)  # data 是一个 list

# === 2. 遍历所有题目，批量处理 ===
for q in data:
    if "title" in q:
        # 替换多个空格为下划线
        q["title"] = q["title"].replace("        ", "__________")  # 8空格 → 10下划线
        # 添加 aishuati 识别用字段 q
        q["q"] = q["title"]

# === 3. 保存到新 JSON 文件 ===
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 处理完成：共 {len(data)} 题")
print("📄 保存文件路径：", os.path.abspath(output_path))
