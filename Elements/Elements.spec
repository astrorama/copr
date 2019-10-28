Summary:        A C++/Python build framework
Name:           Elements
Version:        5.8
Release:        1%{?dist}
License:        LGPLv3
Group:          Development/Tools
Source:         https://github.com/degauden/Elements/archive/%{version}.tar.gz
URL:            https://github.com/degauden/Elements.git
# Remove Example programs and scripts, otherwise they will be installed
Patch0:         elements_remove_examples.patch
# Elements try to guess itself the lib directory, but it does not consider
# 64 bits architectures supported by Fedora. It will override CMAKE_LIB_INSTALL_SUFFIX,
# and stick to its mistaken guess (i.e. /usr/lib for anything that is not x86_64),
# unless this patch is applied
# https://github.com/degauden/Elements/pull/5
Patch1:         elements_do_not_force_install_suffix.patch

BuildRequires: CCfits-devel
BuildRequires: boost-devel >= 1.53
BuildRequires: cfitsio-devel
BuildRequires: cppunit-devel
BuildRequires: fftw-devel
BuildRequires: gmock-devel
BuildRequires: gtest-devel
BuildRequires: log4cpp-devel >= 1.1
BuildRequires: swig
BuildRequires: wcslib-devel
BuildRequires: doxygen

BuildRequires: gcc-c++ > 4.7
BuildRequires: python3
BuildRequires: python3-pytest
BuildRequires: python3-devel
BuildRequires: cmake >= 2.8.5

Requires:      python3

Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%define cmakedir %{_libdir}/cmake/ElementsProject
%define xmldir %{cmakedir}

%define makedir %{_datadir}/%{name}/make
%define confdir %{_datadir}/%{name}
%define auxdir %{_datadir}/auxdir
%define docdir %{_docdir}/%{name}

%description
A C++ base framework for the Euclid Software.


%package devel
Group:  Development/Libraries
Summary: The development part of the %{name} package
Requires: cmake >= 2.8.5
Requires: %{name} = %{version}-%{release}

%description devel
The development part of the %{name} package.


%package doc
Summary: Documentation for package %{name}
Requires: %{name}-devel = %{version}-%{release}

%description doc
Documentation for package %{name}

%prep
%setup -q -c %{name}-%{version}
%patch0 -p1
%patch1 -p1

%build
export VERBOSE=1
EXTRA_CMAKE_FLAGS="-DPYTHON_EXPLICIT_VERSION=3 -DUSE_ENV_FLAGS=ON"
mkdir build
cd build
%cmake -DELEMENTS_BUILD_TESTS=OFF -DSQUEEZED_INSTALL:BOOL=ON -DINSTALL_DOC:BOOL=ON \
    -DUSE_SPHINX=OFF -DPYTHON_EXPLICIT_VERSION=3 --no-warn-unused-cli \
    -DCMAKE_LIB_INSTALL_SUFFIX=%{_lib} ..
%make_build

%install
export VERBOSE=1
cd build
%make_install

%check
export PYTHONPATH="%{buildroot}%{python3_sitearch}"
%{buildroot}/%{_bindir}/CreateElementsProject --help

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{xmldir}/ElementsEnvironment.xml

%{_libdir}/libElementsKernel.so
%{_libdir}/libElementsServices.so

%{_bindir}/CreateElementsProject
%{_bindir}/AddElementsModule
%{_bindir}/AddCppClass
%{_bindir}/AddCppProgram
%{_bindir}/AddPythonProgram
%{_bindir}/AddScript
%{_bindir}/AddPythonModule
%{_bindir}/RemoveCppClass
%{_bindir}/RemoveCppProgram
%{_bindir}/RemovePythonProgram
%{_bindir}/RemovePythonModule
%{_bindir}/ElementsNameCheck
%{_bindir}/GetElementsFiles

%{python3_sitearch}/ELEMENTS_VERSION.py
%{python3_sitearch}/ELEMENTS_INSTALL.py
%{python3_sitearch}/__pycache__/ELEMENTS_*.pyc

%{python3_sitearch}/ElementsKernel/
%{python3_sitearch}/ElementsServices/

%dir %{auxdir}
%{auxdir}/ElementsKernel/

%files devel
%defattr(-,root,root,-)
%{xmldir}/ElementsBuildEnvironment.xml
%{_includedir}/ELEMENTS_VERSION.h
%{_includedir}/ELEMENTS_INSTALL.h
%{_includedir}/ElementsKernel/
%{_includedir}/ElementsServices/

%dir %{cmakedir}
%{cmakedir}/ElementsBuildFlags.cmake
%{cmakedir}/ElementsCoverage.cmake
%{cmakedir}/ElementsDocumentation.cmake
%{cmakedir}/ElementsLocations.cmake
%{cmakedir}/ElementsProjectConfig.cmake
%{cmakedir}/ElementsToolChain.cmake
%{cmakedir}/ElementsToolChainMacros.cmake
%{cmakedir}/ElementsUninstall.cmake
%{cmakedir}/ElementsUtils.cmake
%{cmakedir}/ElementsInfo.cmake
%{cmakedir}/ElementsExports-relwithdebinfo.cmake
%{cmakedir}/ElementsServicesExport.cmake
%{cmakedir}/SGSPlatform.cmake
%{cmakedir}/auxdir
%{cmakedir}/doc
%{cmakedir}/modules
%{cmakedir}/scripts
%{cmakedir}/tests
%{cmakedir}/ElementsExports.cmake
%{cmakedir}/ElementsPlatformConfig.cmake
%{cmakedir}/ElementsKernelExport.cmake
%{cmakedir}/ElementsConfigVersion.cmake
%{cmakedir}/ElementsConfig.cmake

%dir %{makedir}
%{makedir}/Elements.mk

%files doc
%defattr(-,root,root,-)
%license LICENSE.md
%{docdir}

%changelog
* Mon Jul 8 2019 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 5.8
- Bug fixes
- Add the New DataSync service. (Antoine Basset)
- Make the `--config-file` option crash if the file is not present
  It was already the case for the python executables. Now a non-existing
  configuration file passed explicitly on the command line will crash and
  burn.
- Add function to copy and configure an aux file
  (ElementsKernel.Auxiliary.configure)
- Install a .editorconfig file when creating a new project.
- Add new common exit codes for python (ElementsKernel.Exit)
- Add the USE_ENV_FLAGS cmake switch. It allows the environment variables CXXFLAGS
  and CFLAGS to be used by the builder. The default is OFF and these are
  ignored.
- Add the USE_RPM_CMAKE_MACRO cmake switch. It forces the RPM spec file to use the
  %%__cmake RPM macro for the build.
  - By default it is OFF.
  - If is ON, it implies that USE_ENV_FLAGS=ON for consistency with some platform
    RPM build scripts.
- Fix warnings from the compilation of SWIG and Cython generated sources with
  the clang++ compiler
- Add a CMake option (ELEMENTS_DEFAULT_LOGLEVEL) to set the default log level for
  Elements proper messages at compile time. The possible values are
  - INFO: this keeps the same behavior and this is the default for the unsqueeded
    (Euclid-like) installation.
  - DEBUG: this hides the internal Elements messages when running the built executables.
    This is the default for the squeezed installation and the original message can be
    recovered by using the --log-level=DEBUG option of the executable.
- Add an example that opens explicitly a FITS file
- Implement an EXCLUDE option for the Automatic Python Testing.
- Move all the test data from the source tree to the auxdir.

* Fri Apr 12 2019 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 5.6
- Many bug fixes.
- LICENSE.md: add LGPL license file
- cmake/modules/FindRPM.cmake: add the CMake module for the RPM executable
- Add support for the KEEPTEMPDIR env variable for C++. Like for python, the 
  presence of this environment variable will avoid the self-destruction 
  of the temporary files and directories.
- Generalize the usage of the KEEPTEMPDIR variable. It can also be used for
  temporary files and the name of the variable can be chosen in the constructor
- improve the messages in the CMake configure step (Alejandro Álvarez Ayllón).
- ElementsExamples/src/program/FloatPrecisionExample.cpp: Add example to exhibit 
  the floating points characteristics. The float, double and long double properties 
  are printed.
- ElementsKernel/ElementsKernel/Main.h: Factor out the creation of the program 
  manager into a separate macro.
- Add the elements_include_directories CMake macro.    
  Dependending on the HIDE_SYSINC_WARNINGS cmake option (OFF by default), the 
  include directories which are not starting with one of the CMAKE_PROJECT_PATH 
  entries are added with the SYSTEM option. In that case, the "-isystem" gcc command
  line is used instead of the traditional "-I". The warnings coming from these 
  directories are thenignored.
- Add the HIDE_OTHERINC_WARNINGS CMake option. It prevent any compilation warnings 
  coming not only from the system (or third party) libraries, but also from other 
  Elements-based project as well.
- Add fix for the version of rpmbuild >= 4.14. Fix the handling of the byte-compiled 
  files in the rpm creation process.
- Test the existence of sphinxcontrib.napoleon before enabling it.
- Inhibit the python byte-compilation for CVMFS in squeezed install mode. The script 
  that is called by rpmbuild cannot handle a python executable which is not installed 
  in /usr/bin.
- Factor out the creation of the compiled test executable. It allows to create 
  a unit executable of CppUnit or Boost type without adding it to the list of 
  tests. This is useful to delay the usage of the executable in an other project 
  that runs some integration tests.
- ElementsKernel/ElementsKernel/Off64Type.h: Add header file to define off64_t on 
  both Linux and MacOSX.
- Add Travis build configuration file.
- Add the extern declaration for the instantiated templates.
- cmake/modules/FindLibM.cmake: Add CMake module to locate the "m" library. Especially 
  usefully for C code
- Add support for bool on logging of options (Alejandro Álvarez Ayllón).
- make/Elements.mk: Append the CMAKEFLAGS instead of prepending it. It allows 
  to override some of the hardcoded CMake flags from the make library.
- Make the finding of Sphinx REQUIRED if USE_SPHINX is set to ON.
- Use SVG instead of PNG for the dot graphs in doxygen.
- Add the VCS version of the project. This is the number that is produced 
  by the "--version" of the executables. It boils down to the git tag if it exists. 
  Otherwise use a timestamp like 20190329. If git is not present, it falls back
  to the CMake version of the project.
- Add info make target. It is generating a cmake script called cmake_info.cmake 
  that has to be called like "cmake -P cmake_info.cmake". for the moment the following
  CMake informations are provided:
  - the project name
  - the project version
  - the source directory
  - the module list
  - the include directory list
  - the project dependencies
  - the C++ test list with their respective executables.
- ElementsKernel/ElementsKernel/Main.h: Add new macros that allows the passing of 
  arguments to the constructor of the program manager.
- Remove the DB name check.

* Mon Jun 4 2018 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 5.4
- Reduce the top level wrapper Makefile to a minimum. The main library
  is located in the make/Elements.mk file of the framework. The lookup of
  that file is done through the CMAKE_PREFIX_PATH environment variable and
  thus the EuclidEnv package has to be installed on the machine.
- Fix for the version detection of the GCC 7 series and above. The "-dumpversion"
  option is not providing the full version anymore.
- Add support for the numpy include dirs. This is located in the cmake/modules/FindNumPy.cmake
  file.
- Add example for the SWIG interface to numpy.
- Use python3 executable explicitly when calling python scripts.
- Add a new script called GetElementsFile to located any runtime Elements
  resource. Run like:

     E-Run <project_name> <project_version> GetElementsFile -t executable

  in order to get the executable on the path. Please have a look at the
  "--help" option.
- Feature #5886: Add a gitignore template for the creation script that generates an
  Elements-based project
- Feature #5887: Add a --yes option to bypass the interactive part in the creation
  scripts.
- Adapt the CMake code for the new layout of the HealpixCpp distribution
- add a new "cov" make target. This generates a local coverage for the C++ executables.
  Notes:
    - the commands to run it are: make; make test; make cov
    - the BINARY_TAG has to be the cov one (e.g. x86_64-co7-gcc48-cov)
    - the gcov, genhtml, gcovr, lcov tools have to be installed.
- Implementation of the installation and packaging of the documentation
  Notes:
    - A separate RPM file is generated
    - everything is controlled by the INSTALL_DOC CMake option. It is set to OFF by
      default.
    - If INSTALL_DOC ist set to ON, the documentation is automatically built
      together with the default target (all)
- Bug #6131 fixed: Now the configuration file is created under the <conf>
  directory and not under <conf/module_name>
- Add the CONCEPT_CHECKS CMake option. This add the -D_GLIBCXX_CONCEPT_CHECKS
  compile macro. This activate some internal check from the std c++ library. See
  https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_macros.html. It is OFF by
  default.
- Reenable the Elements data modules ad hoc support. Please have a look at the user
  manual.
- Bug #7881 (Nikos/Mher/Hugo): the source hardcoded default values were overriding the
  ones provides in the configuration files.

* Wed Aug 9 2017 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 5.2.1
- Fix the test on the version of sphinx.

* Tue Aug 8 2017 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 5.2
- fix C++ include directories ordering.

* Fri Jul 28 2017 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 5.1-1
- Add the generation of the current Elements module header file
- Use the new getConfigurationPath function to locate the conf files.
- Add the getConfigurationLocations and getAuxiliaryLocations functions. They take 
  into account the /usr/share locations.
- Use the Elements module name as search possibitlity for conf. First default tried 
  is the name of the executable with a ".conf" extension. If not found, 
  <module>/<executable>.conf is tried as a fallback.
- Add the --elements-module-name and --elements-module-version options for the python 
  script creation.
- Add option to forward the CMAKE_PREFIX_PATH to the RPM creation. The option is called 
  RPM_FORWARD_PREFIX_PATH and it is ON by default.
- Fix a bug which was giving priority to the options from the configuration file over 
  the ones from the command line (Nikos Apostolakos)
- Add option to forward the CMAKE_PREFIX_PATH to the RPM creation
- Bug fixed: https://euclid.roe.ac.uk/issues/2305 (Nicolas Morisset)
- Fix the description parsing in the elements_project macro
- Fix issue with wrong default argument for the construction of Program
- Add experimental support for Cython
- Fix issue with incompatible -pg and -pie for executable. It is somehow related 
  with the glibc 2.17. the fix will only be used if the build is "Profile" and 
  the gcc version is less that 5.0. The problem appears on CentOS 7 (and not on 
  Fedora) when linking executables.
- Fix the lookup order in the Environment XML files. There was a bug where the 
  system directories where looked up first.
- Add options to use the sanitize feature of gcc. "-DSANITIZE_OPTIONS=ON" activate 
  the feature. The default is OFF. "-DSANITIZE_STYLE=leak" choose the sanitizer. 
  The default is the "undefined". The undefined checker. Please note that the 
  corresponding sanitizer library must be installed for this feature to work.
- Fix the usage of the "HEAD" keyword for the project version.
- Add options to use distcc and ccache for the build of the rpm. These options are 
  CPACK_USE_CCACHE and CPACK_USE_DISTCC. They are OFF by default.
- Add the -s option for the project and module creation. it allows to remove the 
  implicit dependencies onto Elements and ElementsKernel.
- Pass option to avoid warnings about unused CMake options/variables.
- add new cmake option CPACK_REMOVE_SYSTEM_DEPS to remove system dependencies. Very
  useful when building agains a CVMFS-based RPM db.
- Add correct version of the compiled py files for python 3 in the rpm.

* Thu Apr 06 2017 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 5.0.1-1
- Fix the SPEC file generation for the squeezed installation.

* Mon Mar 06 2017 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 5.0-1
- Doxygen now processes *.md files as well.
- The message from the exceptions is now shown after the stack trace.
- Change the test executable name generated by AddCppClass to contain the _test
  prefix (Nikos Apostolakos)
- Fix the dependency onto a project with a 0 patch version.
- Add name check functionality for the creation scripts. CMake (project and modules),
  libraries and executables must be uniquely named (each). It relies on an URL pointed
  by the ELEMENTS_NAMING_DB_URL environment variable. The ElementsNameCheck script
  can be called directly.
- Fix the stream operator usage with Exception subclasses (Nikos Apostolakos)
- Add the squeezed install option:
  - It performs the installation in the standard CMAKE_INSTALL_PREFIX location (/usr/local
    by default for CMake). It is not multi-versioned
  - The build with the top wrapper Makefile has the -DSQUEEZED_INSTALL=OFF and thus stays in
    the local multiversioned directory layout
  - The build without the wrapper Makefile (with a direct configuration through CMake) is
    performed with the squeezed installation.
- Conform to the -DCMAKE_BUILD_TYPE=... directive on the command line.
  - If it is passed the internal BINARY_TYPE is set accordingly
  - The types to be passed are the canonical ones:  Release, Debug,
    Coverage, Profile, RelWithDebInfo, MinSizeRel.
  - The type to be passed are not case-sensitive.
  - the corresponding BINARY_TAG extensions are: opt, dbg, cov, pro, o2g,min
  - If the BINARY_TAG is in the environment, it is used and the
    CMAKE_BUILD_TYPE is ignored.
- Change the RPM kits naming
  - The squeezed versions get <project>-<version>-1.x86_64.rpm
  - The non-squeezed versions get <project>_<version>-1.0-1.x86_64.rpm
  - The toolchain is also not used if the main build is not using it.
- Re-add the Napoleon Sphinx extension (Nikos Apostolakos)
  - the newest version is embedded in sphinx itself (since version 1.3)
  - before it was an external contribution.
- Add the usage of the cppreference doxygen tagfile 
- Make the -Wfloat-equal warning optional (it is OFF by default)
- Use SOFTWARE_BASE_VAR for the environment variable for base install
  - falls back on EULID_BASE if it exists
  - the final fallback value is /opt/euclid
- Fix AddPythonProgram script which was creating an "scripts" sub-directory. The later was 
  then pruned by the "git clone" command and futher builds were failing.
- Implementation of the ElementsKernel/Configuration.py, ElementsKernel/Auxiliary.py,
  ElementsKernel/Configuration.h, ElementsKernel/Auxiliary.h files that implement:
  - getConfigurtionPath: to get the configuration file in the form "my_prog.conf" or 
    "prefix/my_prog.conf"
  - getAuxiliaryPath: to get the auxiliary file in the form "my_aux" or "prefix/my_aux"

* Mon Dec 05 2016 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 4.1-1
- New version of the documentation generation system
- Add backtrace feature. It displays the stack trace for the crashes. It equips
  the binary built ontop of the ElementsKernel/Program.h class and there is an
  example in the ElementsExamples module. This is especially helpful for the
  forensic study of production crashes.
- Fix valgrind issues for unbalanced new/delete of smart pointers
- Add python ElementsKernel.Temporary.TempEnv class for using a temporary
  environment that will be forgotten after the destruction of the instance.
- Add C++ Elements::TempEnv class that has to same function has the one above
  in python. Very useful for the creation of elaborate tests.
- Add 2 CMake options, SPHINX_BUILD_OPTIONS and SPHINX_APIDOC_OPTIONS ot be
  added to the CMAKEFLAGS environment variable if needed.
- Make the python and internal script compatible with python 3.
- Add script to generate <project>_INSTALL.h header file and python <project>_INSTALL.py
  module that contain the install location.
- Add full RPATH handling for the install location.
- Add a flag to activate C++14 (ELEMENTS_CPP14). It is OFF by default.
- Fix the error reporting of the "make tests" command. Now it returns the exit
  code to the calling shell.
- Add a flag to ignore warnings issued by external included files (like Eigen3
  for example). The flag is called HIDE_SYSINC_WARNINGS and it uses -isystem instead
  of -I for the included external path. It is OFF by default.
- Add the possibility to pass boolean option to the python scripts.
  This is the redmine issue #2708 (Marco Frailis)
- Add the CXX_SUGGEST_OVERRIDE option. It warns about overriding virtual
  functions that are not marked with the override keyword.
- Add the possibility to add an offset for the install location at install time only (for experts only). .
- Add a pure C program example: ElementsExamples/src/CProgram/cutout.c
- Add extra arguments passing to the rpmbuild (RPMBUILD_EXTRA_ARGS).
- Numerous bug fixes and enhancements in the C++, Python and CMake libraries.
- Add a full description of the various Elements build flags to the Wiki at
  http://euclid.roe.ac.uk/projects/elements/wiki/GlobalSwitches.
- Fix Python 3 compatibility issues.

* Tue Mar 22 2016 Hubert Degaudenzi  <Hubert.Degaudenzi@unige.ch> 4.0-1
- This release is foreseen for the Phosphoros version 0.5 project. It
  also include the first integration of the Sphinx/Doxygen implementation.
- Add FindCCache, FindDistCC, FindSphinx, FindValgrind, FindPlantUML CMake modules
- Implement the generation of both Doxygen and Sphinx documentation
- Add the ChangeLog content to the generated SPEC file. The ChangeLog file (this file)
  must be located at the root of the project.
- Add a simple SWIG Python/C++ generation example.
- Add new RemoveCppClass, RemovePythonModule, RemovePythonProgram,
  RemoveCppProgram scripts (Nicolas Morisset).
- Add the CFITSIO_IS_REENTRANT CMake variable. It is computed during the
  configuration and then can be used further in the CMakeLists.txt files
- Add a timeout feature for the pure python tests. This is done by adding the
  TEST_TIMEOUT argument in seconds to the elements_install_python_modules CMake function.
- Update the compilation flags to support security hardening. Please have a
  look at this page https://fedoraproject.org/wiki/Changes/Harden_All_Packages 
  for more information.
- Fix the building of the RPMs file for a custom (general) build directory.
  It doesn't require that the build directory is placed inside the source directory.
- Make the dependency check between projects mandatory. It will break if there
  is an inconsistency in the tree of projects.
- Add global options to enable Doxygen (USE_DOXYGEN) and Sphinx (USE_SPHINX) for
  the automatic documentation generation. They are both ON by default. The is also
  an option for the generation of the Sphinx API documentation (USE_SPHINX_APIDOC)
  which is also ON by default. Please have a look at the user manual for more informations
  about the usage of these switches.
- Make the getAuxPathFile(file_name) python function generic. It can be used to
  locate resources pointed by the directory list in the ELEMENTS_AUX_PATH
  environment variable (Nicolas Morisset).
- Clean up of the main Elements Doxygen page.
- And many bug fixes.

* Tue Feb 09 2016 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 3.10-1
- This release is essentially an update for the release of the EDEN 1.2 version.
- Add CMake build support for various libraries and tools:
  - GSL (issue #1907)
  - HealpixCpp
  - WCS
  - FFTW
  - PyXB
  - Xsd
- Add trivial examples to check that the build works if the following libraries
  are found (their build is conditional):
  - Eigen
  - FFTW
  - GSL
  - HealpixCpp
  - WCS
  - Xerces
- Fix a few issues for the symbol visibility and CMake 3.3
- Add full support for the GCC 5 compiler series.
- Cure redundant sub-namespaces.
- Make the Log4CPP dependency mandatory.
- Fix the CMake detection of the binary executables used at build time. The casing
  of the of the name of the find module file must be the same as the one used for
  the FIND_PACKAGE_HANDLE_STANDARD_ARGS macro.

* Fri Jan 22 2016 Hubert Degaudenzi <Hubert.Degaudenzi@unige.ch> 3.9-1
- This is a release targeted for the ISDC December 2015 Phosphoros Workshop.
- This release is done together with the 1.14 version of the EuclidEnv standalone package
- Here is a short summary of the noticeable changes:
  - Implement the possibility of having generated aux directories (auxdir)
  - Add the main creation helper scripts: CreateElementsProject, AddElementsModule, AddCppProgram, AddCppClass, AddPythonProgram, AddPythonModule (Nicolas Morisset)
  - Fix the build for the MacPort distribution


