from setuptools import setup

setup(
    name="nattle",
    version="0.0.1",
    description="Naval battle",
    url="https://meak.io",
    author="Mehdi Katranji",
    author_email="hello@meak.io",
    license="GPG",
    packages=["nattle"],
    zip_safe=False,
    entry_points={"console_scripts": ["nattle=nattle.nattle:cli"]},
)
