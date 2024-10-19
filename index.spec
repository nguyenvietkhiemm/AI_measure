# -*- mode: python ; coding: utf-8 -*-
import sys
import logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
a = Analysis(['src\\index.py'],
             pathex=['src'],
             binaries=[],
             datas=[
                 ('src/data/raw/*.csv', 'data/raw'),
                 ('src/data/raw/*.xlsx', 'data/raw'),
                 ('src/data/processed/*.csv', 'data/processed'),
                 ('src/data/processed/*.csv', 'data/processed'),
                 ('src/notebooks/*.ipynb', 'notebooks'),
                 ('src/models/*', 'models'),
                 ('src/results/figures/*', 'results/figures'),
                 ('src/results/metrics/*', 'results/metrics'),
                 ('src/results/dataframe/*', 'results/dataframe'),
                 ('src/js/*.js', 'js'),
                 ('src/config.py', '.'),
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=None,
             noarchive=False)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='AI_measure',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True)  # Chỉnh sửa thành False nếu không muốn hiển thị console
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='AI_measure')
