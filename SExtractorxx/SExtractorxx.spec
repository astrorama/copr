%if 0%{?fedora} > 28
%global __python /usr/bin/python3
%else
%global __python /usr/bin/python
%endif

Summary:        SExtractorxx Project
Name:           SExtractorxx
Version:        0.1
Release:        1%{?dist}
License:        LGPL 3.0
Group:          Development/Tools
Source:         https://bintray.com/astrorama/archives/download_file?file_path=sextractorxx-0.1.tar.gz
Vendor:         The Euclid Consortium

%bcond_with doc

%global __brp_mangle_shebangs_exclude /usr/bin/env python
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python_libdir: %define python_libdir %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1,1))")}

BuildRequires: CCfits-devel
BuildRequires: boost-devel >= 1.53
BuildRequires: cfitsio-devel
BuildRequires: cppunit-devel
BuildRequires: Elements-devel = 5.6
BuildRequires: log4cpp-devel
BuildRequires: fftw3-devel
BuildRequires: wcslib-devel
BuildRequires: yaml-cpp-devel
BuildRequires: levmar-devel
BuildRequires: lapack-devel
BuildRequires: blas-devel
BuildRequires: Alexandria-devel = 2.10
BuildRequires: gtest-devel
BuildRequires: gmock-devel


%if 0%{?fedora} > 28
BuildRequires: gcc-c++
BuildRequires: boost-python3-devel
BuildRequires: python3-devel
Requires: python3
%else
BuildRequires: boost-python-devel
BuildRequires: python2-devel
Requires: python
%endif

BuildRequires: gcc > 4.7
BuildRequires: cmake >= 2.8.5
BuildRequires: Alexandria-devel = 2.10
BuildRequires: Elements-devel = 5.6

Requires: Alexandria = 2.10
Requires: Elements = 5.6
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%define bin_tag x86_64-fc28-gcc83-dbg

%define pydir %{python_sitearch}
%define scriptsdir %{_prefix}/bin
%define cmakedir %{_libdir}/cmake/ElementsProject
%define makedir %{_prefix}/share/Elements/make
%define confdir %{_prefix}/share/conf
%define auxdir %{_prefix}/share/auxdir
%define docdir %{_prefix}/share/doc/SExtractorxx
%define xmldir %{_libdir}/cmake/ElementsProject

%if 0%{?fedora} > 28
%define pydyndir %{python_libdir}/lib-dynload
%else
%define pydyndir %{_libdir}/python*/lib-dynload
%endif

%description
Please provide a description of the project.

%package devel
Group:  Development/Libraries
Summary: The development part of the %{name} package
Requires: cmake >= 2.8.5
Requires: %{name} = %{version}-%{release}
Requires: Alexandria-devel = 2.10
Requires: Elements-devel = 5.6

%description devel
The development part of the %{name} package.

%package doc
Summary: Documentation for package %{name}
Requires: %{name}-devel = %{version}-%{release}
Requires: Alexandria-doc = 2.10
Requires: Elements-doc = 5.6

%description doc
Documentation for package %{name}

%package tests
Summary: Tests for %{name}

%description tests
Summary: Tests for %{name}

%prep
%setup -q -c %{name}-%{version}

%build
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
%if 0%{?fedora} > 28
EXTRA_CMAKE_FLAGS="-DPYTHON_EXPLICIT_VERSION=3"
%endif
#
%__mkdir -p $RPM_BUILD_DIR/$BINARY_TAG
cd $RPM_BUILD_DIR/$BINARY_TAG
%cmake  -DSQUEEZED_INSTALL:BOOL=ON -DINSTALL_DOC:BOOL=OFF -DUSE_SPHINX:BOOL=OFF ${EXTRA_CMAKE_FLAGS} --no-warn-unused-cli $RPM_BUILD_DIR/%{name}-%{version}
%__make VERBOSE=1 %{?_smp_mflags} all

%install
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
export CMAKE_PREFIX_PATH=/home/aalvarez/Work/cmake
cd $RPM_BUILD_DIR/$BINARY_TAG
%__make install VERBOSE=1 DESTDIR=$RPM_BUILD_ROOT

%check
export CTEST_OUTPUT_ON_FAILURE=1
export ELEMENTS_NAMING_DB_URL=https://pieclddj00.isdc.unige.ch/elementsnaming
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
export CMAKE_PREFIX_PATH=/home/aalvarez/Work/cmake
cd $RPM_BUILD_DIR/$BINARY_TAG
%__make test

%clean
rm -rf $RPM_BUILD_ROOT

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{xmldir}/SExtractorxxEnvironment.xml
%{_bindir}/sextractor++
%{_libdir}/libModelFitting.so
%{_libdir}/libSEFramework.so
%{_libdir}/libSEImplementation.so
%{_libdir}/libSEMain.so
%{_libdir}/libSEUtils.so
%{confdir}/ExampleModule
%{confdir}/SExtractor.conf
%{pydir}/SEXTRACTORXX_VERSION.py*
%{pydir}/SEXTRACTORXX_INSTALL.py*
%if 0%{?fedora} > 28
%{pydir}/__pycache__/SEXTRACTORXX*
%endif
%{pydir}/sextractorxx
%{pydyndir}/_SExtractorPy.so

%files devel
%defattr(-,root,root,-)
%{xmldir}/SExtractorxxBuildEnvironment.xml
%{_includedir}/SEXTRACTORXX_VERSION.h
%{_includedir}/SEXTRACTORXX_INSTALL.h
%{_includedir}/ModelFitting
%{_includedir}/SEUtils
%{_includedir}/SEFramework
%{_includedir}/SEImplementation
%{_includedir}/SEMain
%dir %{cmakedir}
%{cmakedir}/modules
%{cmakedir}/SExtractorxxExports.cmake
%{cmakedir}/SExtractorxxExports-debug.cmake
%{cmakedir}/SExtractorxxPlatformConfig.cmake
%{cmakedir}/ModelFittingExport.cmake
%{cmakedir}/SEUtilsExport.cmake
%{cmakedir}/SEFrameworkExport.cmake
%{cmakedir}/SEImplementationExport.cmake
%{cmakedir}/SEBenchmarksExport.cmake
%{cmakedir}/SEMainExport.cmake
%{cmakedir}/SExtractorxxConfigVersion.cmake
%{cmakedir}/SExtractorxxConfig.cmake

%if %{with doc}
%files doc
%defattr(-,root,root,-)
%{docdir}
%endif

%files tests
%defattr(-,root,root,-)
%{_bindir}/AperturePhotometry_test
%{_bindir}/AttractorsPartitionStep_test
%{_bindir}/BackgroundConvolution_test
%{_bindir}/BenchConvolution
%{_bindir}/BenchBackgroundConvolution
%{_bindir}/DFT_test
%{_bindir}/Deblending_test
%{_bindir}/DependentParameter_test
%{_bindir}/DetectionFramePixelValues_test
%{_bindir}/DetectionFrameSourceStamp_test
%{_bindir}/DirectConvolution_test
%{_bindir}/EngineParameter_test
%{_bindir}/ExpSigmoidConverter_test
%{_bindir}/ExternalFlag_test
%{_bindir}/FFT_test
%{_bindir}/FunctionalImage_test
%{_bindir}/ImageChunk_test
%{_bindir}/ImageFitsReader_test
%{_bindir}/ImagePsf_test
%{_bindir}/IsophotalFlux_test
%{_bindir}/Lutz_test
%{_bindir}/ManualParameter_test
%{_bindir}/MinAreaPartitionStep_test
%{_bindir}/MirrorImage_test
%{_bindir}/MoffatModelFitting_test
%{_bindir}/MultiThresholdPartitionStep_test
%{_bindir}/NeighbourInfo_test
%{_bindir}/NeutralConverter_test
%{_bindir}/OverlappingBoundariesCriteria_test
%{_bindir}/PaddedImage_test
%{_bindir}/PixelBoundaries_test
%{_bindir}/PixelCentroid_test
%{_bindir}/PixelCoordinate_test
%{_bindir}/PropertyId_test
%{_bindir}/PsfTask_test
%{_bindir}/RecenterImage_test
%{_bindir}/SigmoidConverter_test
%{_bindir}/SimpleSource_test
%{_bindir}/SourceGrouping_test
%{_bindir}/TaskProvider_test
%{_bindir}/TemporaryFile_test
%{_bindir}/TemporaryFitsSource_test
%{_bindir}/TestImage
%{_bindir}/TransformedAperture_test
%{_bindir}/VariablePsf_test
%{_bindir}/VectorImage_test
%{_bindir}/tt
%{_libdir}/libModelFittingBoostTest.so
%{_libdir}/libSEFrameworkBoostTest.so
%{_libdir}/libSEImplementationBoostTest.so
%{_libdir}/libSEUtilsBoostTest.so

%if !0%{?el7}
%{_bindir}/Observable_test
%{_bindir}/Partition_test
%{_bindir}/PropertyHolder_test
%{_bindir}/SourceGroupWithOnDemandProperties_test
%{_bindir}/SourceInterface_test
%{_bindir}/SourceWithOnDemandProperties_test
%endif

