# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['asc_converter.py'],
    pathex=[],
    binaries=[],
    datas=[("C:/Users/Bejlu/OneDrive/Рабочий стол/ASC/.venv/Lib/site-packages/rasterio/gdal_data", 'rasterio/gdal_data')],
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
    name='asc_converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
