from conan import ConanFile
from conan.tools.files import get, patch, copy, chdir
from os.path import join

class MicromodHeader(ConanFile):
    name = "micromod-header"
    package_type = "header-library"

    license = "BSD-3"
    author = "<Shin Umeda> <umeda.shin@gmail.com>"
    url = "https://github.com/DolphinGui/ppackage"
    description = "A header for Picos on micromod"
    topics = ("Embedded", "Raspberry Pi Pico", "ARM")

    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}

    exports_sources = "*.h"
    

    def package(self):
        copy(self, "*", self.export_sources_folder, self.package_folder)
        
    def package_info(self):
        self.buildenv_info.append("PICO_BOARD_HEADER_DIRS", self.package_folder, separator=";")
        self.cpp_info.includedirs = []  # no actual include directories
        self.cpp_info.libdirs = [] # nothing is being built

    def package_id(self):
        self.info.settings.clear()

