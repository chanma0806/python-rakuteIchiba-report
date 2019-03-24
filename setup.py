from setuptools import setup

setup (
    name='rakuten_report',
    version='1.0.0',
    description='make rakuten_report',
    author='Hiroyuiki Maruyama',
    install_requires = ["pandas", "matplotlib", "markdown", "beautifulsoup4", "requests", "selenium", "chromedriver-binary"]
)