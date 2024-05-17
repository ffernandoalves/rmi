import os
from setuptools import setup, Extension, find_packages

# Pequeno teste, msvc / mingw / gnu
# verifique a flag correta para o seu compilador c++
# É necessário c++20 para usar Designated initializers
if os.name == "nt":
    cpp_std = "/std:c++20"
else:
    cpp_std = "-std=c++20"
    
module = Extension(name="rmi.c_rmi",
                    sources=["c_src/c_rmi.cpp"],
                    language='c++',
                    extra_compile_args=[cpp_std]
)

setup(
    ext_modules=[module],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
