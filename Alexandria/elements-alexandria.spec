Summary:        A lightweight C++ utility library
Name:           elements-alexandria
Version:        2.14.1
Release:        2%{?dist}
License:        LGPLv3+
URL:            https://github.com/astrorama/Alexandria.git
Source0:        https://github.com/astrorama/Alexandria/archive/%{version}/%{name}-%{version}.tar.gz
# This file is used to link the documentation to cppreference.com
# It is downloaded from:
# https://upload.cppreference.com/w/File:cppreference-doxygen-web.tag.xml
Source1:        cppreference-doxygen-web.tag.xml

%global elements_version 5.8

BuildRequires: CCfits-devel
BuildRequires: boost-devel >= 1.53
BuildRequires: cfitsio-devel
BuildRequires: cppunit-devel
BuildRequires: elements-devel = %{elements_version}
BuildRequires: log4cpp-devel
# Required for the generation of the documentation
BuildRequires: elements-doc = %{elements_version}
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: texlive-latex
%if 0%{?fedora} >= 30
BuildRequires: texlive-newunicodechar
%endif
BuildRequires: texlive-dvips

BuildRequires: gcc-c++ > 4.7
BuildRequires: cmake >= 2.8.5
%if 0%{?fedora} >= 30
BuildRequires: python3
BuildRequires: python3-pytest
BuildRequires: python3-devel
%else
BuildRequires: python2
BuildRequires: python2-pytest
BuildRequires: python2-devel
%endif

%if 0%{?rhel} && 0%{?rhel} <= 7
Requires: cmake%{?_isa}
%else
Requires: cmake-filesystem%{?_isa}
%endif

%global cmakedir %{_libdir}/cmake/ElementsProject

%global makedir %{_datadir}/Elements/make
%global confdir %{_datadir}/Elements
%global auxdir %{_datadir}/auxdir
%global docdir %{_docdir}/Alexandria

%if 0%{?fedora} >= 30
%global python_sitearch %{python3_sitearch}
%else
%global python_sitearch %{python2_sitearch}
%endif

%description
A lightweight C++ utility library.

%package devel
Summary: The development part of the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: elements-devel%{?_isa} = %{elements_version}

%description devel
The development part of the %{name} package.

%package doc
Summary: Documentation for package %{name}
License: LGPLv3+ and CC-BY-SA
BuildArch: noarch
Requires: elements-doc = %{elements_version}

%description doc
Documentation for package %{name}

%prep
%autosetup -n Alexandria-%{version} -p1

%build
export VERBOSE=1
EXTRA_CMAKE_FLAGS="-DUSE_ENV_FLAGS=ON"
%if 0%{?fedora} >= 30
EXTRA_CMAKE_FLAGS="${EXTRA_CMAKE_FLAGS} -DPYTHON_EXPLICIT_VERSION=3"
%else
EXTRA_CMAKE_FLAGS="${EXTRA_CMAKE_FLAGS} -DPYTHON_EXPLICIT_VERSION=2"
%endif
mkdir build
# Copy cppreference-doxygen-web.tag.xml into the build directory
mkdir -p build/doc/doxygen
cp "%{SOURCE1}" "build/doc/doxygen"
# Build
cd build
%cmake -DELEMENTS_BUILD_TESTS=OFF -DSQUEEZED_INSTALL:BOOL=ON -DINSTALL_DOC:BOOL=ON \
    -DUSE_SPHINX=OFF --no-warn-unused-cli \
    -DCMAKE_LIB_INSTALL_SUFFIX=%{_lib} -DUSE_VERSIONED_LIBRARIES=ON ${EXTRA_CMAKE_FLAGS} \
    ..
%make_build

%install
export VERBOSE=1
cd build
%make_install

%files
%license LICENSE
%{cmakedir}/AlexandriaEnvironment.xml

%{_libdir}/libAlexandriaKernel.so.%{version}
%{_libdir}/libConfiguration.so.%{version}
%{_libdir}/libGridContainer.so.%{version}
%{_libdir}/libNdArray.so.%{version}
%{_libdir}/libMathUtils.so.%{version}
%{_libdir}/libPhysicsUtils.so.%{version}
%{_libdir}/libSOM.so.%{version}
%{_libdir}/libSourceCatalog.so.%{version}
%{_libdir}/libTable.so.%{version}
%{_libdir}/libXYDataset.so.%{version}

%{python_sitearch}/ALEXANDRIA_VERSION.py*
%{python_sitearch}/ALEXANDRIA_INSTALL.py*
%if 0%{?fedora} >= 30
%{python_sitearch}/__pycache__/ALEXANDRIA*.pyc
%endif

%files devel
%{_libdir}/libAlexandriaKernel.so
%{_libdir}/libConfiguration.so
%{_libdir}/libGridContainer.so
%{_libdir}/libNdArray.so
%{_libdir}/libMathUtils.so
%{_libdir}/libPhysicsUtils.so
%{_libdir}/libSOM.so
%{_libdir}/libSourceCatalog.so
%{_libdir}/libTable.so
%{_libdir}/libXYDataset.so

%{_includedir}/ALEXANDRIA_VERSION.h
%{_includedir}/ALEXANDRIA_INSTALL.h
%{_includedir}/AlexandriaKernel/
%{_includedir}/Table/
%{_includedir}/XYDataset/
%{_includedir}/GridContainer/
%{_includedir}/NdArray/
%{_includedir}/SourceCatalog/
%{_includedir}/Configuration/
%{_includedir}/MathUtils/
%{_includedir}/PhysicsUtils/
%{_includedir}/SOM/

%{cmakedir}/AlexandriaBuildEnvironment.xml
%{cmakedir}/AlexandriaExports.cmake
%{cmakedir}/AlexandriaExports-relwithdebinfo.cmake
%{cmakedir}/AlexandriaPlatformConfig.cmake
%{cmakedir}/AlexandriaKernelExport.cmake
%{cmakedir}/TableExport.cmake
%{cmakedir}/XYDatasetExport.cmake
%{cmakedir}/GridContainerExport.cmake
%{cmakedir}/NdArrayExport.cmake
%{cmakedir}/SourceCatalogExport.cmake
%{cmakedir}/ConfigurationExport.cmake
%{cmakedir}/MathUtilsExport.cmake
%{cmakedir}/PhysicsUtilsExport.cmake
%{cmakedir}/SOMExport.cmake
%{cmakedir}/AlexandriaConfigVersion.cmake
%{cmakedir}/AlexandriaConfig.cmake

%files doc
%license LICENSE
%{docdir}

%changelog
* Mon Jan 13 2020 Alejandro Alvarez Ayllon <alejandro.alvarezayllon@unige.ch> 2.14.1-2
- Fix conditional dependency on cmake-filesystem
- Add LICENSE file to the main package

* Fri Jan 10 2020 Alejandro Alvarez Ayllon <alejandro.alvarezayllon@unige.ch> 2.14.1-1
- Initial RPM
