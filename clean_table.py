import sys
import os
import re

def clean_line(line):
    # Удаляем метку слева, например "101-C" или "101-C|"
    line = re.sub(r"^\s*\d+\-C\s*\|?", "", line)
    # Удаляем метку справа, например "C-101"
    line = re.sub(r"\|?\s*C\-\d+\s*$", "", line)
    # Удаляем префикс: например "100-|", "102|", и т.п.
    line = re.sub(r"^\s*\d+\S*\|", "", line)
    # Удаляем суффикс: например "|- 100", "| 100", или просто "|"
    line = re.sub(r"\|\-?\s*\d*\s*$", "", line)
    return line.strip()

def contains_numbers(line):
    return re.search(r"\d", line) is not None

def process_file(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Очищаем и фильтруем строки с числами
    cleaned_lines = [
        clean_line(line) for line in lines
        if contains_numbers(line) and clean_line(line).strip() != ""
    ]

    # Добавим шапку
    header = [
        "ncols",
        "nrows",
        "xllcenter",
        "yllcenter",
        "cellsize",
        "NODATA_value",
    ]

    output_path = os.path.splitext(input_path)[0] + "_cleaned.asc"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(header + cleaned_lines))

    print(f"✅ Файл с шапкой сохранён как: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Перетащи файл в этот .exe или вызови через командную строку:")
        print("clean_table.exe путь_к_файлу.txt")
    else:
        process_file(sys.argv[1])