from setuptools import setup, find_packages

setup(
    name="System Contable",
    version="1.0.0",
    packages=find_packages(where="App"),
    package_dir={"": "App"},
    install_requires=[
        "PySide6",
        "openpyxl"
    ],
    entry_points={
        "console_scripts": [
            "system-contable=App.gui.Gui_Login:main"
        ]
    },
)