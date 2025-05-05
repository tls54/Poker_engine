from setuptools import setup, Extension
from setuptools import find_packages
import pybind11
import sys
import platform

# Extra compiler args depending on platform
extra_compile_args = ["-std=c++17"]
extra_link_args = []

extra_compile_args = ["-O3", "-std=c++17"]
if platform.system() == "Darwin":
    extra_compile_args.append("-stdlib=libc++")
elif platform.system() == "Windows":
    extra_compile_args = ["/O2", "/std:c++17"]  # Use /O2 for MSVC (equivalent to -O2); /Ox includes /O2

ext_modules = [
    Extension(
        "poker_engine.hand_eval",
        sources=["poker_engine/hand_eval.cpp"],
        include_dirs=[pybind11.get_include(), pybind11.get_include(user=True)],
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )
]

setup(
    name="poker_engine",
    version="0.1.0",
    packages=find_packages(),
    ext_modules=ext_modules,
    zip_safe=False,
)
