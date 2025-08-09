# PyInstaller hook for audioop module
# This ensures audioop is properly included in Windows builds

from PyInstaller.utils.hooks import collect_all

# Force include audioop module
hiddenimports = ['audioop']

# Also collect any related audio modules
datas, binaries, more_hiddenimports = collect_all('audioop')
hiddenimports.extend(more_hiddenimports)
