from setuptools import setup

with open("requirements.txt", "r") as handle:
    requirements = handle.readlines()

setup(
    install_requires=requirements
)