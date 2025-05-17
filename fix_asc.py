import re
import sys
import os

def fix_line(line):
    return " ".join(re.findall(r"\d+\.\d{3}", line)) + "\n"

def fix_file(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header = lines[:6]
    data_lines = lines[6:]
    fixed_data_lines = [fix_line(line) for line in data_lines]
    fixed_lines = header + fixed_data_lines

    base, ext = os.path.splitext(input_path)
    output_path = base + "_fixed" + ext

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)

    print(f"Исправленный файл сохранён как: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Пожалуйста, перетащите .asc файл на этот exe или запустите через командную строку:")
        print("Пример: fix_asc.exe путь_к_файлу.asc")
    else:
        fix_file(sys.argv[1])
