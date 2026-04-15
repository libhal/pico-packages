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
from conan.tools.files import get, patch, chdir
from pathlib import Path


class Picotool(ConanFile):
    name = "picotool"
    package_type = "application"
    license = "BSD-3"
    author = "<Shin Umeda> <umeda.shin@gmail.com>"
    url = "https://github.com/libhal/pico-packages"
    description = "The Raspberry Pi Picotool repackaged for conan"
    topics = ("Embedded", "Raspberry Pi Pico", "ARM")
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "patches/*"

    def requirements(self):
        DEPENDENCIES_VERSION = self.conan_data["dependencies"][self.version]
        self.output.error(f"{DEPENDENCIES_VERSION}")
        for dep, version in DEPENDENCIES_VERSION.items():
            self.requires(f"{dep}/{version}")

        self.requires("libusb/1.0.29")
        self.requires(f"picosdk/{self.version}")

    def layout(self):
        cmake_layout(self, src_folder="picotool")

    def source(self):
        strip = not self.version.startswith(
            "2.1"
        )  # only 2.2.0 and on have normal directories
        with chdir(self, ".."):
            # Downloading two sources is kinda bad, but unfortunately picotool requires the sdk for some reason
            get(
                self,
                **self.conan_data["picotool_sources"][self.version],
                destination="picotool",
                strip_root=strip,
            )
            EXPORT_SOURCE = Path(self.export_sources_folder)
            PATCH_NAME = f"{self.version}-ptool.patch"
            PATCH_FILE = EXPORT_SOURCE / "patches" / PATCH_NAME
            patch(
                self,
                patch_file=str(PATCH_FILE),
                base_path=EXPORT_SOURCE / "picotool",
            )

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
