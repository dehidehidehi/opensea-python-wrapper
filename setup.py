from pathlib import Path
from setuptools import setup, find_packages


def read_requirements_txt() -> list:
    base = Path(__file__).parent
    with open(base / 'requirements.txt', 'r') as r:
        return r.read().splitlines()


setup(
    name='opensea_api_wrapper',
    author='COJEAN Kévin',
    author_email='digitalexmachina+openseaapiwrapper@gmail.com',
    python_requires='>=3.9',
    install_requires=read_requirements_txt(),
    packages=find_packages(),
)