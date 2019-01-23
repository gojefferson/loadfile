from setuptools import setup

setup(
    name="loadfile",
    version="0.1",
    py_modules=["loadfile"],
    install_requires=["Click", "chardet", "colorama"],
    entry_points="""
        [console_scripts]
        loadfile=loadfile:loadfile
    """,
)
