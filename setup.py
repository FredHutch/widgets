from setuptools import setup
import os

with open("requirements.txt", "r") as handle:
    requirements = handle.readlines()

if __name__ == "__main__":
    setup(
        install_requires=requirements,
        data_files=[
            (
                'templates',
                [
                    os.path.join("src/widgets/templates", fn)
                    for fn in os.listdir("src/widgets/templates")
                ]
            )
        ]
    )
