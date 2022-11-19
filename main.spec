block_cipher = None


a = Analysis(['main.py'],
             pathex=['gocqhttpbot\\botstart\\controller\\GroupController.py', 'gocqhttpbot\\botstart\\controller\\GroupHanderController.py', 'gocqhttpbot\\botstart\\controller\\GuildController.py', 'gocqhttpbot\\botstart\\controller\\SkyController.py', 'gocqhttpbot\\botstart\\controller\\WebBotController.py', 'gocqhttpbot\\botstart\\dao\\get_db_test.py', 'gocqhttpbot\\botstart\\dao\\GroupHanderDao.py', 'gocqhttpbot\\botstart\\entity\\CQcode.py', 'gocqhttpbot\\botstart\\entity\\GroupEntity.py', 'gocqhttpbot\\botstart\\entity\\GuildEntity.py', 'gocqhttpbot\\botstart\\entity\\xmlEntity.py', 'gocqhttpbot\\botstart\\impl\\animeImpl.py', 'gocqhttpbot\\botstart\\impl\\blind_box.py', 'gocqhttpbot\\botstart\\impl\\gatherImpl.py', 'gocqhttpbot\\botstart\\impl\\guildImpl.py', 'gocqhttpbot\\botstart\\impl\\hireImpl.py', 'gocqhttpbot\\botstart\\impl\\menuImpl.py', 'gocqhttpbot\\botstart\\impl\\otherImpl.py', 'gocqhttpbot\\botstart\\impl\\RadishImpl.py', 'gocqhttpbot\\botstart\\impl\\skyImpl.py', 'gocqhttpbot\\botstart\\impl\\wfImpl.py', 'gocqhttpbot\\botstart\\impl\\yuleImpl.py', 'gocqhttpbot\\botstart\\RunThread.py', 'gocqhttpbot\\botstart\\util\\CmdUtil.py', 'gocqhttpbot\\botstart\\util\\init.py', 'gocqhttpbot\\botstart\\util\\memeImgGenerate.py', 'gocqhttpbot\\botstart\\util\\permissions.py', 'gocqhttpbot\\botstart\\util\\SignUtil.py', 'gocqhttpbot\\botstart\\util\\textToImg.py', 'gocqhttpbot\\botstart\\util\\wfUtils.py', 'gocqhttpbot\\botstart\\util\\wordUtil.py', 'E:\\pythonProject\\test1\\gocqhttpbot'],
             binaries=[],
             datas=[],
             hiddenimports=['GroupController', 'GroupHanderController', 'GuildController', 'SkyController', 'WebBotController', 'get_db_test', 'GroupHanderDao', 'CQcode', 'GroupEntity', 'GuildEntity', 'xmlEntity', 'animeImpl', 'blind_box', 'gatherImpl', 'guildImpl', 'hireImpl', 'menuImpl', 'otherImpl', 'RadishImpl', 'skyImpl', 'wfImpl', 'yuleImpl', 'RunThread', 'CmdUtil', 'init', 'memeImgGenerate', 'permissions', 'SignUtil', 'textToImg', 'wfUtils', 'wordUtil'],             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )