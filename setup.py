from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',  # 아이콘 있으면 넣기
    'plist': {
        'CFBundleName': 'ADOFAI Key Viewer',
        'CFBundleDisplayName': 'ADOFAI Key Viewer',
        'CFBundleVersion': '1.0',
        'CFBundleShortVersionString': '1.0',
    },
    'packages': ['pygame', 'pynput'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
