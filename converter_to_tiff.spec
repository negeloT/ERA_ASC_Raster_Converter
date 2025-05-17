# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['converter_to_tiff.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Путь для rasterio/gdal_data
        ("C:/Users/Bejlu/OneDrive/Рабочий стол/ASC/.venv/Lib/site-packages/rasterio/gdal_data", 'rasterio/gdal_data'), 
        
        # Путь для pyproj/proj_dir
        ("C:/Users/Bejlu/OneDrive/Рабочий стол/ASC/.venv/Lib/site-packages/pyproj/proj_dir/share/proj", 'pyproj/proj')
    ],
    hiddenimports=[
        'rasterio._io',
        'rasterio.sample',
        'rasterio.vrt',
        'rasterio.transform',
        'rasterio.crs',
        'rasterio.env',
        'rasterio._features'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='converter_to_tiff',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Устанавливаем False для скрытия консоли при запуске
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
