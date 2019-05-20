# -*- mode: python -*-

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['/root/code/verifier/Verifier/'],
             binaries=[],
             datas=[('logs/discord.log','logs/'),
		      ('instance/db/db.json','instance/db'),
		      ('instance/modules','instance/modules'),
                    ('instance/db/sessions.json','instance/db'),
		      ('instance/config/.env','instance/config/'),
		      ('instance/config/text.json','instance/config/'),
		      ('instance/config/config.json','instance/config/'),
                    ('instance/config/license.json','instance/config/'),
                    ('instance/config/dbconfig.json','instance/config/'),
                    ('instance/config/wordpress.json','instance/config/'),
                    ('instance/config/verify_text.txt','instance/config/')],
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
               name='instanceid')