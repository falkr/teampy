import codecs
import os.path
from distutils.core import setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


package_name = "teampy"

setup(
    name=package_name,
    packages=[package_name],
    version=get_version("{}/__init__.py".format(package_name)),
    description="Tools for Team-Based Learning",
    install_requires=[
        "pyyaml>=5.3",
        "colorama>=0.4.3",
        "click>=7.0",
        "numpy",
        "pandas",
        "xlrd>=1.1.0",
        "openpyxl",
        "progressbar2",
        "latex>=0.7",
    ],
    package_data={"": ["*.tex", "*.pdf"],},
    include_package_data=True,
    author="Frank Alexander Kraemer",
    author_email="kraemer.frank@gmail.com",
    license="GPLv3",
    url="https://github.com/falkr/teampy",
    download_url="https://github.com/falkr/teampy/archive/0.2.tar.gz",
    keywords=["education"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "teampy=teampy.command_line_setup:teampy",
            "rat=teampy.command_line_rat:rat",
        ]
    },
)
