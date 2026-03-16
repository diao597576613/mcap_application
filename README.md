# Mcap Examples（独立示例库）

从 [mcap](https://github.com/foxglove/mcap) 的 example 目录抽离的独立代码库，用于按样例编写和试验 MCAP 相关代码。**本仓库使用 Conan 2**；mcap 主仓仍用 Conan 1，二者不互通。

## 依赖

- **CMake** ≥ 3.10
- **Conan 2**（包管理，用于拉取 mcap 2.1.x 等）
- **C++17** 编译器（GCC、Clang 或 MSVC）

## 安装 Conan 2

```bash
pip install --upgrade conan
conan --version   # 应为 2.x
```

首次使用建议配置默认 profile（GCC 下避免 ABI 问题）。**Conan 2 没有 `profile update`**，需直接改 profile 文件：

```bash
conan profile detect
# 查看 default profile 路径，编辑该文件，在 [settings] 下增加一行：
#   compiler.libcxx=libstdc++11
conan profile path default
```

或用一行追加（bash）：

```bash
echo "compiler.libcxx=libstdc++11" >> "$(conan profile path default)"
```

（若 `[settings]` 已存在，请用编辑器打开该文件，在 `[settings]` 块内手动加入 `compiler.libcxx=libstdc++11`。）

## 编译

### 1. 安装 Conan 依赖并生成 CMake 配置

```bash
mkdir -p build && cd build
conan install .. --output-folder=. --build=missing
```

### 2. 配置并编译

```bash
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

### 一键（在项目根目录）

```bash
./scripts/build.sh
```

或使用 VS Code/Cursor 任务：`Ctrl+Shift+B`（见 `.vscode/tasks.json`，需改为 Conan 2 命令）。

## 产物

- **build/**：构建目录，其中 `compile_commands.json` 用于 IDE 智能提示与跳转。
- 可执行文件在 `build/` 下，例如：
  - `bag2mcap`、`mcapdump`、`rotatemcap`
  - `build/protobuf/`：`example_protobuf_writer`、`example_protobuf_dynamic_reader`、`example_protobuf_static_reader`、`example_protobuf_unit_tests`
  - `build/jsonschema/`：`example_json_writer`、`example_json_reader`

## 自动补全与跳转

- 本仓库已设置 **CMAKE_EXPORT_COMPILE_COMMANDS=ON**，构建后会在 `build/compile_commands.json` 生成编译数据库。
- VS Code/Cursor 的 C++ 扩展会通过 `.vscode/settings.json` 使用该文件，实现代码补全、跳转到定义等。**使用前请先完成一次编译**。

## 目录结构

```
.
├── CMakeLists.txt          # 根 CMake（find_package + 各 target）
├── conanfile.py            # Conan 2 依赖与 generate
├── bag2mcap.cpp, mcapdump.cpp, rotatemcap.cpp
├── protobuf/               # Protobuf 读写示例
├── jsonschema/             # JSON Schema 示例
├── .vscode/
└── scripts/build.sh
```

## 为什么用 Conan 2？

- **mcap 2.1.x** 只在 **Conan 2** 的 center（如 center2.conan.io）上提供，Conan 1 的 center 最高只到 mcap 1.4.1。
- 本仓库已迁到 Conan 2（`conanfile.py` 用 `from conan import ConanFile`、CMake 用 `find_package` + `conan_toolchain.cmake`），与 mcap 主仓的 Conan 1 配置**不兼容**，主仓仍可继续用 Conan 1 + editable mcap。

## 单独管理说明

- 本仓库可单独 clone、修改、提交，不依赖 mcap 主仓源码。
- 依赖由 Conan 2 拉取（mcap、protobuf、nlohmann_json、catch2），无需本地 mcap 源码或 editable。
