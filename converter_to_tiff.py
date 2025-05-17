import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
import rasterio
from pyproj import CRS

def main(asc_file):
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно

    # Запрашиваем EPSG код
    try:
        epsg_code = simpledialog.askinteger("EPSG код", "Введите EPSG код системы координат:")
        if epsg_code is None:
            messagebox.showwarning("Отмена", "EPSG код не введён.")
            return
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при вводе EPSG кода: {e}")
        return

    tiff_path = os.path.splitext(asc_file)[0] + ".tif"

    # Установка CRS
    try:
        crs = CRS.from_epsg(epsg_code)
    except Exception as e:
        messagebox.showerror("Ошибка CRS", f"Неверный EPSG код: {e}")
        return

    # Конвертация в GeoTIFF
    try:
        with rasterio.open(asc_file) as src:
            profile = src.profile.copy()
            profile.update({
                "driver": "GTiff",
                "crs": crs
            })

            with rasterio.open(tiff_path, "w", **profile) as dst:
                dst.write(src.read(1), 1)

        messagebox.showinfo("Успех", f"GeoTIFF создан:\n{tiff_path}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при создании GeoTIFF: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        messagebox.showerror("Ошибка", "Файл не передан. Перетащите .asc файл на .exe файл.")
    else:
        asc_file = sys.argv[1]
        main(asc_file)
