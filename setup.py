from setuptools import setup, find_packages

setup(
    name="kopf_example",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["kopf", "debugpy", "pyyaml", "sqlalchemy"],
    extras_require={
        "development": ["mypy", "black[d]", "flake8", "pytest", "devtools"]
    },
)
