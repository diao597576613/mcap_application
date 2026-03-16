#!/usr/bin/env bash
# Conan 2 构建：需先安装 Conan 2（pip install conan）
set -e
cd "$(dirname "$0")/.."
mkdir -p build
cd build
# 生成 toolchain 与 *-config.cmake（GCC 下建议 profile 里 compiler.libcxx=libstdc++11）
conan install .. --output-folder=. --build=missing
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build .
