from setuptools import setup

setup(
    name="bdd",
    version="0.1.0",
    description="A CLI tool for completing boot.dev lessons",
    packages=["bdd"],
    python_requires=">=3.10",
    install_requires=["click", "requests"],
    entry_points={"console_scripts": ["bdd=bdd.cli:cli"]},
)
