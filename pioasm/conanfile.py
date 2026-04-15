# MIT License
#
# Copyright (c) 2025 Shin Umeda
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get, patch, chdir, rmdir
import shutil
from pathlib import Path


class PioASM(ConanFile):
    name = "pioasm"
    package_type = "application"
    license = "BSD-3"
    author = "<Shin Umeda> <umeda.shin@gmail.com>"
    url = "https://github.com/libhal/pico-packages"
    description = "The Raspberry Pi Pico Pio Assembler repackaged for conan"
    topics = ("Embedded", "Raspberry Pi Pico", "ARM")
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "patches/*"

    def build_requirements(self):
        self.tool_requires("cmake/[^4.0.0]")

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version],
            destination='sdkroot', strip_root=not self.version.startswith('2.1'))
        EXPORT_SOURCE = Path(self.export_sources_folder)
        PATCH_FILE = EXPORT_SOURCE / "patches" / f"{self.version}-pioasm.patch"
        SDKROOT = Path('sdkroot')
        patch(self, patch_file=str(PATCH_FILE), base_path=SDKROOT)
        with chdir(self, SDKROOT / "tools" / "pioasm"):
            DESTINATION = self.source_folder
            for files in Path('.').iterdir():
                shutil.move(str(files), DESTINATION)
        rmdir(self, SDKROOT)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.cache_variables['PIOASM_VERSION_STRING'] = str(self.version)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        pass
