# Mcap Examples（独立示例库）

从 [mcap](https://github.com/foxglove/mcap) 的 example 目录抽离的独立代码库，用于按样例编写和试验 MCAP 相关代码。

## 依赖

- **CMake** ≥ 3.10
- **Conan** 1.x（包管理）
- **C++17** 编译器（GCC、Clang 或 MSVC）

## 编译

### 1. 安装 Conan 依赖并配置

```bash
mkdir -p build && cd build
# 必须指定 compiler.libcxx=libstdc++11，与 GCC 5+ 默认 ABI 一致，否则会链接报 undefined reference to ... [abi:cxx11]
conan install .. --build=missing -s compiler.libcxx=libstdc++11
```

### 2. 配置并编译

```bash
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
```

### 一键（在项目根目录）

```bash
./scripts/build.sh
```

或使用 VS Code/Cursor 任务：`Ctrl+Shift+B`（见 `.vscode/tasks.json`）。

## 产物

- **build/**：构建目录，其中 `compile_commands.json` 用于 IDE 智能提示与跳转。
- 可执行文件在 `build/` 下，例如：
  - `bag2mcap`、`mcapdump`、`rotatemcap`
  - `build/protobuf/`：`example_protobuf_writer`、`example_protobuf_dynamic_reader`、`example_protobuf_static_reader`、`example_protobuf_unit_tests`
  - `build/jsonschema/`：`example_json_writer`、`example_json_reader`

## 自动补全与跳转

- 本仓库已设置 **CMAKE_EXPORT_COMPILE_COMMANDS=ON**，构建后会在 `build/compile_commands.json` 生成编译数据库。
- VS Code/Cursor 的 C++ 扩展会通过 `.vscode/settings.json` 使用该文件，实现：
  - 代码补全（IntelliSense）
  - 跳转到定义（F12）
  - 查找引用、悬停提示等

**使用前请先完成一次编译**，否则 `compile_commands.json` 不存在，补全可能不完整。

## 目录结构

```
.
├── CMakeLists.txt          # 根 CMake
├── conanfile.py            # Conan 依赖
├── bag2mcap.cpp
├── mcapdump.cpp
├── rotatemcap.cpp
├── protobuf/               # Protobuf 读写示例
│   ├── proto/              # .proto 定义
│   ├── writer.cpp, dynamic_reader.cpp, static_reader.cpp, unit_tests.cpp
│   └── CMakeLists.txt
├── jsonschema/             # JSON Schema 示例
│   └── ...
├── .vscode/                # 编辑器配置（补全、任务）
└── scripts/
    └── build.sh            # 一键构建脚本
```

## 为什么在原来的 mcap 里能编过，拷贝出来就链接报错？

常见原因是 **C++ 标准库 ABI 不一致**：

- 在原仓库里，mcap 可能是 **Editable** 或和 example 一起在同一套 CMake/Conan 下构建，用的同一套 `compiler.libcxx`（多为 `libstdc++11`）。
- 拷贝出来后，Conan 用的是你本机默认 profile；若默认是 **compiler.libcxx=libstdc++**（旧 ABI），而当前 GCC 编译本工程时用的是 **libstdc++11**（新 ABI），则 Conan 提供的 libprotobuf 与当前编译的符号不匹配，就会出现 `undefined reference to ... [abi:cxx11]`。

**处理办法**：安装依赖时显式指定与当前编译器一致的 ABI，例如：

```bash
conan install .. --build=missing -s compiler.libcxx=libstdc++11
```

或永久改默认 profile（可选）：

```bash
conan profile update settings.compiler.libcxx=libstdc++11 default
```

之后如需清缓存重装 protobuf，可加 `--build=protobuf`。

## 单独管理说明

- 本仓库可单独 git clone、修改、提交，不依赖 mcap 主仓库。
- 依赖通过 Conan 拉取（mcap、protobuf、nlohmann_json、catch2），无需手动装 mcap 源码。
- 若将来要同步上游 example 的改动，可把本仓库的 remote 指回 mcap 的 example 目录或按需 cherry-pick/手动合并。
