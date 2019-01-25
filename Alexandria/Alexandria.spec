# -*- rpm-spec -*-

Summary:        Alexandria Project
Name:           Alexandria
Version:        2.10
Release:        1%{?dist}
License:        Public Domain
Group:          Development/Tools
Source:         https://github.com/nikoapos/Alexandria/archive/2.10.tar.gz
Vendor:         The Euclid Consortium

Patch0:         Elements_5.4.patch

%bcond_with doc

%global __brp_mangle_shebangs_exclude /usr/bin/env python
%global __python /usr/bin/python 



BuildRequires: CCfits-devel
BuildRequires: boost-devel >= 1.53
BuildRequires: cfitsio-devel
BuildRequires: cppunit-devel
BuildRequires: Elements-devel = 5.4
BuildRequires: log4cpp-devel

%if 0%{?fedora} > 28
BuildRequires: gcc-c++
%endif
BuildRequires: gcc > 4.7
BuildRequires: cmake >= 2.8.5
BuildRequires: Elements-devel = 5.4


Requires: python
Requires: Elements = 5.4
Requires(post):    /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%define bin_tag x86_64-fc28-gcc82-o2g
%define _prefix /usr
%define build_dir_name ../../mnt/tmp/tmpze9yyphs/Alexandria/builddir

%define libdir %{_prefix}/lib64
%define pydir %{_prefix}/lib64/python2.7/site-packages
%define pydyndir %{_prefix}/lib64/python2.7/lib-dynload
%define scriptsdir %{_prefix}/bin
%define cmakedir %{_prefix}/lib64/cmake/ElementsProject
%define makedir %{_prefix}/share/Elements/make
%define confdir %{_prefix}/share/conf
%define auxdir %{_prefix}/share/auxdir
%define docdir %{_prefix}/share/doc/Alexandria
%define xmldir %{_prefix}/lib64/cmake/ElementsProject



%description
Please provide a description of the project.

%package devel
Group:  Development/Libraries
Summary: The development part of the %{name} package
Requires: cmake >= 2.8.5
Requires: %{name} = %{version}-%{release}
Requires: Elements-devel = 5.4

%description devel
The development part of the %{name} package.

%package doc
Summary: Documentation for package %{name}
Requires: %{name}-devel = %{version}-%{release}
Requires: Elements-doc = 5.4

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
#
cd $RPM_BUILD_DIR/$BINARY_TAG
%__make install VERBOSE=1 DESTDIR=$RPM_BUILD_ROOT

%check
export CTEST_OUTPUT_ON_FAILURE=1
export ELEMENTS_NAMING_DB_URL=https://pieclddj00.isdc.unige.ch/elementsnaming
export BINARY_TAG=%{bin_tag}
export VERBOSE=1
#
cd $RPM_BUILD_DIR/$BINARY_TAG
%__make test

%clean
rm -rf $RPM_BUILD_ROOT

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%{xmldir}/AlexandriaEnvironment.xml
%{libdir}/libAlexandriaKernel.so
%{libdir}/libConfiguration.so
%{libdir}/libGridContainer.so
%{libdir}/libNdArray.so
%{libdir}/libMathUtils.so
%{libdir}/libPhysicsUtils.so
%{libdir}/libSOM.so
%{libdir}/libSourceCatalog.so
%{libdir}/libTable.so
%{libdir}/libXYDataset.so
%{pydir}/ALEXANDRIA_VERSION.py
%{pydir}/ALEXANDRIA_VERSION.pyo
%{pydir}/ALEXANDRIA_VERSION.pyc
%{pydir}/ALEXANDRIA_INSTALL.py
%{pydir}/ALEXANDRIA_INSTALL.pyo
%{pydir}/ALEXANDRIA_INSTALL.pyc

%files devel
%defattr(-,root,root,-)
%{xmldir}/AlexandriaBuildEnvironment.xml
%{_includedir}/ALEXANDRIA_VERSION.h
%{_includedir}/ALEXANDRIA_INSTALL.h
%{_includedir}/AlexandriaKernel
%{_includedir}/Table
%{_includedir}/XYDataset
%{_includedir}/GridContainer
%{_includedir}/NdArray
%{_includedir}/SourceCatalog
%{_includedir}/Configuration
%{_includedir}/MathUtils
%{_includedir}/PhysicsUtils
%{_includedir}/SOM
%dir %{cmakedir}
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

%if %{with doc}
%files doc
%defattr(-,root,root,-)
%{docdir}
%endif

%files tests
%{_bindir}/AlexandriaKernel_ThreadPool_test
%{_bindir}/AsciiParser_test
%{_bindir}/AsciiReaderHelper_test
%{_bindir}/AsciiReader_test
%{_bindir}/AsciiWriterHelper_test
%{_bindir}/AsciiWriter_test
%{_bindir}/CastVisitor_test
%{_bindir}/CatalogConfig_test
%{_bindir}/CatalogFromTable_test
%{_bindir}/Catalog_test
%{_bindir}/ColumnDescription_test
%{_bindir}/ColumnInfo_test
%{_bindir}/ConfigManager_test
%{_bindir}/Configuration_test
%{_bindir}/Coordinates_test
%{_bindir}/CosmologicalDistances_test
%{_bindir}/CosmologicalParameters_test
%{_bindir}/FileSystemProvider_test
%{_bindir}/FitsParser_test
%{_bindir}/FitsReaderHelper_test
%{_bindir}/FitsReader_test
%{_bindir}/FitsWriterHelper_test
%{_bindir}/FitsWriter_test
%{_bindir}/GirdAxis_serialization_test
%{_bindir}/GridAxis_test
%{_bindir}/GridCellManagerTraits_test
%{_bindir}/GridConstructionHelper_test
%{_bindir}/GridContainer_test
%{_bindir}/GridIndexHelper_test
%{_bindir}/NdArray_test
%{_bindir}/PhotometricBandMappingConfig_test
%{_bindir}/PhotometryAttributeFromRow_test
%{_bindir}/PhotometryCatalogConfig_test
%{_bindir}/Photometry_test
%{_bindir}/ProgramOptionsHelper_test
%{_bindir}/QualifiedName_test
%{_bindir}/Row_test
%{_bindir}/SOM_SOM_test
%{_bindir}/SimpsonsRule_test
%{_bindir}/SourceCatalog_all_attribute_tests
%{_bindir}/SourceCatalog_all_tests
%{_bindir}/Source_test
%{_bindir}/SpecZCatalogConfig_test
%{_bindir}/SpectroscopicRedshiftAttributeFromRow_test
%{_bindir}/SpectroscopicRedshift_test
%{_bindir}/Table_test
%{_bindir}/XYDataset_CachedProvider_test
%{_bindir}/XYDataset_test
%{_bindir}/function_all_tests
%{_bindir}/interpolation_all_tests
%{_bindir}/serialize_test
%{_bindir}/tuple_serialization_test
%{libdir}/libAlexandriaKernelBoostTest.so
%{libdir}/libConfigurationBoostTest.so
%{libdir}/libGridContainerBoostTest.so
%{libdir}/libNdArrayBoostTest.so
%{libdir}/libMathUtilsBoostTest.so
%{libdir}/libPhysicsUtilsBoostTest.so
%{libdir}/libSOMBoostTest.so
%{libdir}/libSourceCatalogBoostTest.so
%{libdir}/libTableBoostTest.so
%{libdir}/libXYDatasetBoostTest.so
