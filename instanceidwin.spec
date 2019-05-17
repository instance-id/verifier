# -*- mode: python -*-

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['C:\\Users\\Home\\Documents\\Verifier'],
             binaries=[],
             datas=[('config/config.json','config/'),
                    ('config/dbconfig.json','config/'),
                    ('config/license.json','config/'),
                    ('config/wordpress.json','config/'),
                    ('config/verify_text.txt','config/'),
                    ('config/text.json','config/'),
                    ('instance/modules','instance/modules'),
                    ('instance/db/db.json','instance/db'),
                    ('instance/db/sessions.json','instance/db'),
                    ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='verifier',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='verifier')
