#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os
import shutil


class GnuPlotConan(ConanFile):
    name = "gnuplot"
    version = "5.2.5"
    description = "GNUplot"
    topics = "conan", "gnuplot"
    url = "https://github.com/zehome/conan-gnuplot"
    homepage = "http://www.gnuplot.info/"
    author = "Laurent Coustet <ed@zehome.com>"
    license = "GPL-3.0-only"
    generators = "txt"
    settings = "os", "compiler", "build_type", "arch"
    # Possible requires: qt, lua, gd, pdflib, cairo, caca, debug
    _source_subfolder = "gnuplot-src"

    def source(self):
        source_url = "https://sourceforge.net/projects/gnuplot/files/gnuplot"
        tools.get("{0}/{1}/gnuplot-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = "gnuplot-{0}".format(self.version)
        if os.path.exists(self._source_subfolder):
            shutil.rmtree(self._source_subfolder)
        os.rename(extracted_dir, self._source_subfolder)
        if self.settings.os == "Windows":
            tools.replace_in_file(
                os.path.join(self._source_subfolder, "config", "msvc", "Makefile"),
                "DEBUG = 0",
                "PLATFORM = X64\r\nDEBUG = 0")

    def build(self):
        if self.settings.os == "Windows":
            with tools.chdir(os.path.join(self._source_subfolder, "config", "msvc")):
                with tools.environment_append({"PLATFORM": "X64"}):
                    self.run("{0} && set && nmake".format(
                        tools.vcvars_command(self.settings)))
        else:
            with tools.chdir(self._source_subfolder):
                autotools = AutoToolsBuildEnvironment(self)
                autotools.configure(args=["--without-qt", "--without-cairo", "--without-lua", "--without-readline", "--without-latex", "--without-libcerf", "--without-x"])
                autotools.make()
                # autotools.install()

    def package(self):
        if self.settings.os == "Windows":
            self.copy("*.exe", src=os.path.join(self._source_subfolder, "config", "msvc"), dst="bin")
        else:
            self.copy("gnuplot*", src=os.path.join(self._source_subfolder, "src"), dst="bin")
