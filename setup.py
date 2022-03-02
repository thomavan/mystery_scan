from setuptools import setup, Extension
import setuptools
import os
import sys

def get_pybind_include():
    import pybind11
    return pybind11.get_include()

src_path = os.path.abspath('./src')

if 'ZEBRA_SCANNER_SRC_PATH' not in os.environ:
    os.environ['ZEBRA_SCANNER_SRC_PATH'] = src_path
else:
    src_path = os.environ['ZEBRA_SCANNER_SRC_PATH']

with open("README.rst", "r") as fh:
    long_description = fh.read()

source_files = [
    os.path.join(src_path, 'BoostPythonCoreScanner.cpp')
]

zebra_scanner_module = Extension("mystery_scan",
    include_dirs=[
        '/usr/include/mystery_scan',
        get_pybind_include(),
        src_path
    ],
    library_dirs=['/usr/lib/mystery_scan/corescanner'],
    libraries=['cs-client', 'cs-common', 'pugixml'],
    sources=source_files,
    extra_compile_args=['-Wno-deprecated', '-std=c++11', '-fvisibility=hidden']
)

setup(
    name="mystery_scan",
    version="v0.2.5",
    author="Tho Van",
    author_email="thomas.vanniere@cbc.lu",
    description="Scan barcodes with a zebra barcode scanner",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/thomavan/mystery_scan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules=[zebra_scanner_module]
)
