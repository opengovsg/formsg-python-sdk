import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="formsg-python-sdk",
    version="0.1.2",
    description="Python SDK for Forms",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="Open Government Products",
    author_email="chinying@open.gov.sg",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["formsg", "formsg.util"],
    include_package_data=True,
    install_requires=["PyNaCl>=1.5.0", "requests>=2.27.0"],
    entry_points={},
)
