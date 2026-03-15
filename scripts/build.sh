#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
mkdir -p build
cd build
# 必须与当前 GCC 的默认 ABI 一致（GCC 5+ 默认 libstdc++11），否则会报 undefined reference to ... [abi:cxx11]
conan install .. --build=missing -s compiler.libcxx=libstdc++11
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
