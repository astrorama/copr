Summary:        A program that extracts a catalog of sources from astronomical images.
Name:           sourcextractor++
Version:        0.8
Release:        1%{?dist}
License:        LGPLv3+
URL:            https://github.com/astrorama/sourcextractorplusplus
Source0:        https://github.com/astrorama/sourcextractorplusplus/archive/%{version}/%{name}-%{version}.tar.gz
# This file is used to link the documentation to cppreference.com
# It is downloaded from:
# https://upload.cppreference.com/w/File:cppreference-doxygen-web.tag.xml
Source1:        cppreference-doxygen-web.tag.xml
# These binaries are not intended for users, so we drop them from the build
Patch0:         remove_benchmarks.patch
Patch1:         remove_testimage.patch
# These example conf files are left over from the creation of the project
# https://github.com/astrorama/SourceXtractorPlusPlus/commit/506f67e556c8b7b20a5f39450c00cafaa174b8cf
Patch2:         remove_example_conffiles.patch
# Add /etc to the search paths for configuration files
# https://github.com/astrorama/SourceXtractorPlusPlus/pull/213
Patch3:         config_etc.patch

%global elements_version 5.8
%global alexandria_version 2.14.1

BuildRequires: CCfits-devel
BuildRequires: boost-devel >= 1.53
BuildRequires: cfitsio-devel
BuildRequires: cppunit-devel
BuildRequires: log4cpp-devel
BuildRequires: fftw-devel >= 3
BuildRequires: levmar-devel >= 2.5
BuildRequires: wcslib-devel
%if 0%{?fedora} >= 30
BuildRequires: gsl-devel >= 2.2.1
%endif
BuildRequires: elements-devel = %{elements_version}
BuildRequires: elements-alexandria-devel = %{alexandria_version} 
# Required for the generation of the documentation
BuildRequires: elements-doc = %{elements_version}
BuildRequires: elements-alexandria-doc = %{alexandria_version}
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
BuildRequires: boost-python3-devel >= 1.53
%else
BuildRequires: python2
BuildRequires: python2-pytest
BuildRequires: python2-devel
BuildRequires: boost-python-devel >= 1.53
%endif

%if 0%{?rhel} && 0%{?rhel} <= 7
Requires: cmake%{?_isa}
%else
Requires: cmake-filesystem%{?_isa}
%endif

%global cmakedir %{_libdir}/cmake/ElementsProject

%if 0%{?fedora} >= 30
%global python_sitearch %{python3_sitearch}
%global python_sitelib %{python3_sitelib}
%else
%global python_sitearch %{python2_sitearch}
%global python_sitelib %{python2_sitelib}
%endif

%description
%{name} is a program that extracts a catalog of sources from astronomical images.
It is the successor to the original SExtractor package.

%package devel
Summary: The development part of the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: elements-devel%{?_isa} = %{elements_version}
Requires: elemenets-alexandria%{?_isa} = %{alexandria_version}

%description devel
The development part of the %{name} package.

%package doc
Summary: Documentation for package %{name}
License: LGPLv3+ and CC-BY-SA
BuildArch: noarch
Requires: elements-doc = %{elements_version}
Requires: elements-alexandria-doc = %{alexandria_version}

%description doc
Documentation for package %{name}

%prep
%autosetup -n SourceXtractorPlusPlus-%{version} -p1

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

# Because of limitations of Elements, ++ can not be used as part of the
# project name. For consistency, we rename some of the destination directories
# to sourcextractor++
mv %{buildroot}/%{_docdir}/SourceXtractorPlusPlus %{buildroot}/%{_docdir}/sourcextractor++

# Similarly, move the configuration file to /etc
mkdir -p %{buildroot}/%{_sysconfdir}
mv %{buildroot}/%{_datadir}/conf/sourcextractor++.conf %{buildroot}/%{_sysconfdir}/sourcextractor++.conf
rm -r %{buildroot}/%{_datadir}/conf/

%files
%license LICENSE
%{cmakedir}/SourceXtractorPlusPlusEnvironment.xml

%{_bindir}/sourcextractor++
%config(noreplace) %{_sysconfdir}/sourcextractor++.conf

%{_libdir}/libModelFitting.so.%{version}
%{_libdir}/libSEFramework.so.%{version}
%{_libdir}/libSEImplementation.so.%{version}
%{_libdir}/libSEMain.so.%{version}
%{_libdir}/libSEUtils.so.%{version}

%{python_sitearch}/SOURCEXTRACTORPLUSPLUS_VERSION.py*
%{python_sitearch}/SOURCEXTRACTORPLUSPLUS_INSTALL.py*
%{python_sitearch}/sourcextractor/
%{python_sitearch}/../lib-dynload/_SourceXtractorPy.so

%if 0%{?fedora} >= 30
%{python_sitearch}/__pycache__/SOURCEXTRACTORPLUSPLUS*.pyc
%endif

%files devel
%{_libdir}/libModelFitting.so
%{_libdir}/libSEFramework.so
%{_libdir}/libSEImplementation.so
%{_libdir}/libSEMain.so
%{_libdir}/libSEUtils.so

%{_includedir}/SOURCEXTRACTORPLUSPLUS_VERSION.h
%{_includedir}/SOURCEXTRACTORPLUSPLUS_INSTALL.h
%{_includedir}/ModelFitting/
%{_includedir}/SEFramework/
%{_includedir}/SEImplementation/
%{_includedir}/SEMain/
%{_includedir}/SEUtils/

%{cmakedir}/SourceXtractorPlusPlusBuildEnvironment.xml
%{cmakedir}/SourceXtractorPlusPlusExports.cmake
%{cmakedir}/SourceXtractorPlusPlusExports-relwithdebinfo.cmake
%{cmakedir}/SourceXtractorPlusPlusPlatformConfig.cmake
%{cmakedir}/SourceXtractorPlusPlusConfig.cmake
%{cmakedir}/SourceXtractorPlusPlusConfigVersion.cmake
%{cmakedir}/ModelFittingExport.cmake
%{cmakedir}/SEFrameworkExport.cmake
%{cmakedir}/SEImplementationExport.cmake
%{cmakedir}/SEMainExport.cmake
%{cmakedir}/SEUtilsExport.cmake
%{cmakedir}/modules/*.cmake

%files doc
%license LICENSE
%{_docdir}/sourcextractor++

%changelog
* Fri Jan 31 2020 Alejandro Alvarez Ayllon <a.alvarezayllon@gmail.com> 0.8-1
- New RPM

