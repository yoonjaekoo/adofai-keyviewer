from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
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
