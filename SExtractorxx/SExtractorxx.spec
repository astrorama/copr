# -*- rpm-spec -*-

Summary:        SExtractorxx Project
Name:           SExtractorxx
Version:        0.1
Release:        1%{?dist}
License:        Public Domain
Group:          Development/Tools
Source:         https://bintray.com/ayllon/sextractorxx/download_file?file_path=sextractorxx-0.1.tar.gz
Vendor:         The Euclid Consortium

Patch0:         elements_alexandria.patch

%bcond_with doc

%global __brp_mangle_shebangs_exclude /usr/bin/env python
%global __python /usr/bin/python 



BuildRequires: CCfits-devel
BuildRequires: boost-devel >= 1.53
BuildRequires: cfitsio-devel
BuildRequires: cppunit-devel
BuildRequires: Elements-devel = 5.4
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

%if 0%{?el7}
BuildRequires: boost-python
%else
BuildRequires: boost-python2
%endif
BuildRequires: python2-devel

%if 0%{?fedora} > 28
BuildRequires: gcc-c++
%endif
BuildRequires: gcc > 4.7
BuildRequires: cmake >= 2.8.5
BuildRequires: Alexandria-devel = 2.10
BuildRequires: Elements-devel = 5.4


Requires: python
Requires: Alexandria = 2.10
Requires: Elements = 5.4
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%define bin_tag x86_64-fc28-gcc82-dbg
%define _prefix /usr
%define build_dir_name ../../home/aalvarez/Work/Projects/SExtractorxx/.copr/builddir

%define libdir %{_prefix}/lib64
%define pydir %{_prefix}/lib64/python2.7/site-packages
%define pydyndir %{_prefix}/lib64/python2.7/lib-dynload
%define scriptsdir %{_prefix}/bin
%define cmakedir %{_prefix}/lib64/cmake/ElementsProject
%define makedir %{_prefix}/share/Elements/make
%define confdir %{_prefix}/share/conf
%define auxdir %{_prefix}/share/auxdir
%define docdir %{_prefix}/share/doc/SExtractorxx
%define xmldir %{_prefix}/lib64/cmake/ElementsProject


%description
Please provide a description of the project.

%package devel
Group:  Development/Libraries
Summary: The development part of the %{name} package
Requires: cmake >= 2.8.5
Requires: %{name} = %{version}-%{release}
Requires: Alexandria-devel = 2.10
Requires: Elements-devel = 5.4

%description devel
The development part of the %{name} package.

%package doc
Summary: Documentation for package %{name}
Requires: %{name}-devel = %{version}-%{release}
Requires: Alexandria-doc = 2.10
Requires: Elements-doc = 5.4

%description doc
Documentation for package %{name}

%package tests
Summary: Tests for %{name}

%description tests
Summary: Tests for %{name}

%prep
%setup -q -n sextractorxx-%{version}
%patch0 -p1

%build
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
%__mkdir -p $RPM_BUILD_DIR/$BINARY_TAG
cd $RPM_BUILD_DIR/$BINARY_TAG
%cmake  -DSQUEEZED_INSTALL:BOOL=ON -DINSTALL_DOC:BOOL=OFF --no-warn-unused-cli $RPM_BUILD_DIR/sextractorxx-%{version}
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
%{_bindir}/SExtractor
%{libdir}/libModelFitting.so
%{libdir}/libSEFramework.so
%{libdir}/libSEImplementation.so
%{libdir}/libSEMain.so
%{libdir}/libSEUtils.so
%{confdir}/ExampleModule
%{confdir}/SExtractor.conf
%{pydir}/SEXTRACTORXX_VERSION.py
%{pydir}/SEXTRACTORXX_VERSION.pyo
%{pydir}/SEXTRACTORXX_VERSION.pyc
%{pydir}/SEXTRACTORXX_INSTALL.py
%{pydir}/SEXTRACTORXX_INSTALL.pyo
%{pydir}/SEXTRACTORXX_INSTALL.pyc
%{pydir}/sextractorxx

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
%{_bindir}/BenchConvolution
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
%{_bindir}/ImageChunk_test
%{_bindir}/ImageFitsReader_test
%{_bindir}/ImagePsf_test
%{_bindir}/IsophotalFlux_test
%{_bindir}/Lutz_test
%{_bindir}/ManualParameter_test
%{_bindir}/MinAreaPartitionStep_test
%{_bindir}/MirrorImage_test
%{_bindir}/MultiThresholdPartitionStep_test
%{_bindir}/NeighbourInfo_test
%{_bindir}/NeutralConverter_test
%{_bindir}/OverlappingBoundariesCriteria_test
%{_bindir}/PaddedImage_test
%{_bindir}/PixelBoundaries_test
%{_bindir}/PixelCentroid_test
%{_bindir}/PixelCoordinate_test
%{_bindir}/PointModelFitting_test
%{_bindir}/PropertyId_test
%{_bindir}/PsfTask_test
%{_bindir}/RecenterImage_test
%{_bindir}/SigmoidConverter_test
%{_bindir}/SimpleModelFitting_test
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
%{libdir}/libModelFittingBoostTest.so
%{libdir}/libSEFrameworkBoostTest.so
%{libdir}/libSEImplementationBoostTest.so
%{libdir}/libSEUtilsBoostTest.so

%if !0%{?el7}
%{_bindir}/Observable_test
%{_bindir}/Partition_test
%{_bindir}/PropertyHolder_test
%{_bindir}/SourceGroupWithOnDemandProperties_test
%{_bindir}/SourceInterface_test
%{_bindir}/SourceWithOnDemandProperties_test
%endif

