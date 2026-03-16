# Conan 2：使用 pip install conan 安装，mcap 2.1.x 在 Conan 2 center (center2.conan.io)
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain


class McapExamplesConan(ConanFile):
    name = "mcap_examples"
    version = "0.1"
    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"
    requires = [
        "mcap/2.1.1",
        "protobuf/3.21.12",  # 3.21.1 在部分 Conan 2 remote 不可用，改用 3.21.12
        "nlohmann_json/3.11.2",
        "catch2/3.5.2",  # 2.14.0 在 Conan 2 center 已不可用，改用 3.x
    ]

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def configure(self):
        self.settings.compiler.cppstd = "17"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
