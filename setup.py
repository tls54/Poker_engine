from setuptools import setup, Extension
from setuptools import find_packages
import pybind11

ext_modules = [
    Extension(
        "poker_engine.hand_eval",
        sources=["poker_engine/hand_eval.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++"
    )
]

setup(
    name="poker_engine",
    version="0.1.0",
    packages=find_packages(),
    ext_modules=ext_modules,
    zip_safe=False,
)