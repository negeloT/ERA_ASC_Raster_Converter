import sys
import os
import re
import tkinter as tk
from tkinter import simpledialog, messagebox
import pyproj
from pyproj import CRS
import os
import sys

# Устанавливаем GDAL_DATA вручную
try:
    import rasterio
    gdal_data_path = os.path.join(os.path.dirname(rasterio.__file__), 'gdal_data')
    if os.path.exists(gdal_data_path):
        os.environ['GDAL_DATA'] = gdal_data_path
    else:
        print("⚠️ gdal_data не найден по пути:", gdal_data_path)
except Exception as e:
    print(f"Не удалось установить GDAL_DATA: {e}")

# ---------------------- Clean Table ----------------------

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

def clean_table(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = [
        clean_line(line) for line in lines
        if contains_numbers(line) and clean_line(line).strip() != ""
    ]

    output_path = os.path.splitext(input_path)[0] + "_cleaned.asc"
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

    return output_path

# ---------------------- Fix ASC ----------------------

def fix_line(line):
    return " ".join(re.findall(r"\d+\.\d{3}", line)) + "\n"

def fix_file(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Вставка заголовка будет позже, сейчас просто фиксируем данные
    header = lines[:6]
    data_lines = lines[6:]
    fixed_data_lines = [fix_line(line) for line in data_lines]
    fixed_lines = header + fixed_data_lines

    output_path = os.path.splitext(input_path)[0] + "_fixed.asc"
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(fixed_lines)

    return output_path

# ---------------------- UTM Conversion ----------------------

def get_utm_zone(x, y):
    proj = pyproj.Proj(proj="utm", zone=int((x + 180) / 6) + 1, ellps="WGS84")
    utm_x, utm_y = proj(x, y)
    return utm_x, utm_y

# ---------------------- Main Workflow ----------------------

def main(txt_file):
    root = tk.Tk()
    root.withdraw()

    try:
        ncols = simpledialog.askinteger("ncols", "Введите кол-во столбцов:")
        nrows = simpledialog.askinteger("nrows", "Введите кол-во строк:")
        cellsize = float(simpledialog.askstring("cellsize", "Введите размер шага:"))
        xrp = float(simpledialog.askstring("x РП", "Введите коорд. X РП:"))
        yrp = float(simpledialog.askstring("y РП", "Введите коорд. Y РП:"))
        width = float(simpledialog.askstring("ширина", "Введите длину РП (L):"))
        height = float(simpledialog.askstring("высота", "Введите ширину РП (B):"))
        xll = float(simpledialog.askstring("xllcenter", "Введите геогр. коорд. X центра (долгота):"))
        yll = float(simpledialog.askstring("yllcenter", "Введите геогр. коорд. Y центра: (широта)"))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка ввода: {e}")
        return

    utm_x, utm_y = get_utm_zone(xll, yll)

    cleaned_path = clean_table(txt_file)

    # Добавляем заголовок
    with open(cleaned_path, "r", encoding='utf-8') as f:
        data = f.read()

    xllcenter = utm_x + xrp - width / 2 - cellsize / 2
    yllcenter = utm_y + yrp - height / 2 - cellsize / 2

    header = f"""ncols         {ncols}
nrows         {nrows}
xllcenter     {xllcenter:.3f}
yllcenter     {yllcenter:.3f}
cellsize      {cellsize}
NODATA_value  -9999
"""

    with open(cleaned_path, "w", encoding='utf-8') as f:
        f.write(header + data)

    final_path = fix_file(cleaned_path)

    # ---------------------- Конвертация ASC → GeoTIFF и задание UTM CRS ----------------------
    import rasterio

    # Путь к .asc файлу
    asc_path = final_path
    tiff_path = os.path.splitext(asc_path)[0] + ".tif"

    # Создаем CRS через Proj
    zone = int((xll + 180) / 6) + 1
    is_northern = yll >= 0

    # Определяем UTM зону по координатам
    epsg_code = 32600 + zone if is_northern else 32700 + zone

    # Создаем CRS через EPSG
    crs = CRS.from_epsg(epsg_code)

    print("Создание GeoTIFF...")

    try:
        with rasterio.open(asc_path) as src:
            profile = src.profile.copy()
            profile.update({
                "driver": "GTiff",
                "crs": crs
            })

            with rasterio.open(tiff_path, "w", **profile) as dst:
                dst.write(src.read(1), 1)

        messagebox.showinfo("Успех", f"GeoTIFF создан:\n{tiff_path}\nUTM Zone: {zone}")

    except Exception as e:
        messagebox.showerror("Ошибка при создании GeoTIFF", str(e))

    os.remove(cleaned_path)
    messagebox.showinfo("Готово", f"Файл сохранён как:\n{final_path}")

# ---------------------- Entry Point ----------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        messagebox.showwarning("Нет файла", "Перетащите txt файл на exe")
