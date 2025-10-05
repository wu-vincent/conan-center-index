import os

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.files import (
    apply_conandata_patches,
    copy,
    export_conandata_patches,
    get,
    rmdir,
)
from conan.tools.scm import Version

required_conan_version = ">=1.53.0"


class LLVMClangConan(ConanFile):
    name = "llvm-clang"
    description = "Clang is a compiler front-end for the C family of languages (C, C++ and Objective-C)"
    license = "Apache-2.0 WITH LLVM-exception"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/llvm/llvm-project/blob/main/clang"
    topics = ("llvm", "clang")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_xml2": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_xml2": True,
    }

    @property
    def _version_major(self):
        return Version(self.version).major

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires(f"llvm-core/{self.version}")
        if self.options.with_xml2:
            self.requires("libxml2/[>=2.12.5 <3]")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, 17)

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.20 <5]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version]["clang"], strip_root=True)
        get(
            self,
            **self.conan_data["sources"][self.version]["cmake"],
            strip_root=True,
            destination=os.path.join(self.export_sources_folder, "cmake"),
        )

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.cache_variables["CLANG_BUILT_STANDALONE"] = True
        tc.cache_variables["LLVM_INCLUDE_TESTS"] = False
        tc.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(
            self,
            "LICENSE.txt",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses"),
        )
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Clang")
        self.cpp_info.set_property("cmake_target_name", "Clang::Clang")
