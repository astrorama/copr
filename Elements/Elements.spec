# -*- rpm-spec -*-

Summary:        Elements Project
Name:           Elements
Version:        5.4
Release:        1%{?dist}
License:        Public Domain
Group:          Development/Tools
Source:         https://github.com/degauden/Elements/archive/5.4.tar.gz
Vendor:         The Euclid Consortium

Patch0:         disable_tests.patch

%bcond_with doc

%global __brp_mangle_shebangs_exclude /usr/bin/env python
%global __python /usr/bin/python 



BuildRequires: CCfits-devel
BuildRequires: boost-devel >= 1.53
BuildRequires: cfitsio-devel
BuildRequires: cppunit-devel
BuildRequires: fftw-devel
BuildRequires: gmock-devel
BuildRequires: gtest-devel
BuildRequires: log4cpp-devel >= 1.1
BuildRequires: python2
BuildRequires: python2-devel
BuildRequires: python2-pytest
BuildRequires: swig
BuildRequires: wcslib-devel

%if 0%{?fedora} > 28
BuildRequires: gcc-c++
BuildRequires: python3-pytest
BuildRequires: python3-devel
%endif
BuildRequires: gcc > 4.7
BuildRequires: cmake >= 2.8.5



Requires: python

Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%define bin_tag x86_64-fc28-gcc82-o2g
%define _prefix /usr
%define build_dir_name ../../mnt/tmp/tmpv7p8q5nh/Elements/builddir

%define libdir %{_prefix}/lib64
%define pydir %{_prefix}/lib64/python2.7/site-packages
%define pydyndir %{_prefix}/lib64/python2.7/lib-dynload
%define scriptsdir %{_prefix}/bin
%define cmakedir %{_prefix}/lib64/cmake/ElementsProject
%define makedir %{_prefix}/share/Elements/make
%define confdir %{_prefix}/share/conf
%define auxdir %{_prefix}/share/auxdir
%define docdir %{_prefix}/share/doc/Elements
%define xmldir %{_prefix}/lib64/cmake/ElementsProject



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

%package tests
Summary: Tests for %{name}

%description tests
Tests for %{name}


%prep
%setup -q
%patch0 -p1

%build
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
#
%__mkdir -p $RPM_BUILD_DIR/$BINARY_TAG
cd $RPM_BUILD_DIR/$BINARY_TAG
%cmake  -DSQUEEZED_INSTALL:BOOL=ON -DINSTALL_DOC:BOOL=OFF --no-warn-unused-cli $RPM_BUILD_DIR/%{name}-%{version}
%__make VERBOSE=1 %{?_smp_mflags} all

%install
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
cd $RPM_BUILD_DIR/$BINARY_TAG
%__make install VERBOSE=1 DESTDIR=$RPM_BUILD_ROOT

%check
export CTEST_OUTPUT_ON_FAILURE=1
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
cd $RPM_BUILD_DIR/$BINARY_TAG
%__make test

%clean
rm -rf $RPM_BUILD_ROOT

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{xmldir}/ElementsEnvironment.xml
%{libdir}/libElementsKernel.so
%{libdir}/libElementsKernelBoostTest.so
%{scriptsdir}/CreateElementsProject
%{scriptsdir}/AddElementsModule
%{scriptsdir}/AddCppClass
%{scriptsdir}/AddCppProgram
%{scriptsdir}/AddPythonProgram
%{scriptsdir}/AddScript
%{scriptsdir}/AddPythonModule
%{scriptsdir}/RemoveCppClass
%{scriptsdir}/RemoveCppProgram
%{scriptsdir}/RemovePythonProgram
%{scriptsdir}/RemovePythonModule
%{scriptsdir}/ElementsNameCheck
%{scriptsdir}/GetElementsFiles
%{auxdir}/ElementsKernel
%{pydir}/ELEMENTS_VERSION.py
%{pydir}/ELEMENTS_VERSION.pyo
%{pydir}/ELEMENTS_VERSION.pyc
%{pydir}/ELEMENTS_INSTALL.py
%{pydir}/ELEMENTS_INSTALL.pyo
%{pydir}/ELEMENTS_INSTALL.pyc
%{pydir}/ElementsKernel

%files devel
%defattr(-,root,root,-)
%{xmldir}/ElementsBuildEnvironment.xml
%{_includedir}/ELEMENTS_VERSION.h
%{_includedir}/ELEMENTS_INSTALL.h
%{_includedir}/ElementsKernel
%{_includedir}/ElementsExamples
%dir %{cmakedir}
%{cmakedir}/Elements-squeeze.spec.in
%{cmakedir}/Elements.spec.in
%{cmakedir}/ElementsBuildFlags.cmake
%{cmakedir}/ElementsCoverage.cmake
%{cmakedir}/ElementsDocumentation.cmake
%{cmakedir}/ElementsLocations.cmake
%{cmakedir}/ElementsProjectConfig.cmake
%{cmakedir}/ElementsToolChain.cmake
%{cmakedir}/ElementsToolChainMacros.cmake
%{cmakedir}/ElementsUninstall.cmake
%{cmakedir}/ElementsUtils.cmake
%{cmakedir}/SGSPlatform.cmake
%{cmakedir}/auxdir
%{cmakedir}/cmake_uninstall.cmake.in
%{cmakedir}/doc
%{cmakedir}/modules
%{cmakedir}/scripts
%{cmakedir}/tests
%{cmakedir}/ElementsExports.cmake
%{cmakedir}/ElementsExports-relwithdebinfo.cmake
%{cmakedir}/ElementsPlatformConfig.cmake
%{cmakedir}/ElementsKernelExport.cmake
%{cmakedir}/ElementsExamplesExport.cmake
%{cmakedir}/ElementsConfigVersion.cmake
%{cmakedir}/ElementsConfig.cmake
%dir %{makedir}
%{makedir}/Elements.mk

%if %{with doc}
%files doc
%defattr(-,root,root,-)
%{docdir}
%endif

%files tests
%defattr(-,root,root,-)
%{_bindir}/*_test
%{_bindir}/*Example*
%{libdir}/*Examples*
%{pydir}/*Example*
%{pydyndir}/*Example*
%{scriptsdir}/*_test
%{scriptsdir}/*Example*
%{confdir}/CppProgramExample.conf
%{confdir}/ElementsExamples

%changelog
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


