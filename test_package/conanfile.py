
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain

class CompressorRecipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    options = {"board": ["ANY"], "platform": ["ANY"], "variant": ["ANY"]}
    generators = "VirtualBuildEnv"

    def requirements(self):
        self.requires("picosdk/2.2.0")

    def build_requirements(self):
        self.tool_requires("pioasm/2.2.0")
        self.tool_requires("picotool/2.2.0")
    
    def generate(self):
        tc = CMakeToolchain(self)
        if str(self.options.platform).startswith("rp2"):
            if self.options.board:
                tc.cache_variables["PICO_BOARD"] = str(self.options.board)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        defs = {
            "CMAKE_ASM_FLAGS_INIT": "-mcpu=cortex-m33 -mfloat-abi=soft",
        }
        cmake.configure(variables = defs)
        cmake.build()
