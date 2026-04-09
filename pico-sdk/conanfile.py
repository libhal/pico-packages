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
from conan.tools.files import get, patch, copy, chdir
from pathlib import Path


class PicoSDK(ConanFile):
    name = "picosdk"
    package_type = "static-library"
    license = "BSD-3"
    author = "<Shin Umeda> <umeda.shin@gmail.com>"
    url = "https://github.com/libhal/pico-packages"
    description = "The Raspberry Pi Pico C/C++ SDK repackaged for conan"
    topics = ("Embedded", "Raspberry Pi Pico", "ARM")
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}
    exports_sources = "patches/*"

    def source(self):
        strip = not self.version.startswith('2.1')
        get(self, **self.conan_data["sources"]
            [self.version]["sdk"], strip_root=strip)
        EXPORT_SOURCE = Path(self.export_sources_folder)
        PATCH_FILE = EXPORT_SOURCE / "patches" / f"{self.version}-psdk.patch"
        patch(self, patch_file=str(PATCH_FILE))
        with chdir(self, "lib"):
            get(self, **self.conan_data["sources"][self.version]
                ["tinyusb"], destination="tinyusb", strip_root=strip)

    def package(self):
        copy(self, "*", self.export_sources_folder, self.package_folder)

    def package_info(self):
        self.buildenv_info.define("PICO_SDK_PATH", self.package_folder)
        self.cpp_info.includedirs = []  # no actual include directories
        self.cpp_info.libdirs = []  # nothing is being built

    def package_id(self):
        self.info.settings.clear()
