%define package_name     mpc
%define package_version  %{_version}
%define package_release  %{_release}

Summary:        Norlook toolchain - GNU MPC package
Name:           norlook-toolchain-%{package_name}
Version:        %{package_version}
Release:        %{package_release}%{?dist}
Group:          Unspecified
License:        LGPL-3.0
BuildArch:      x86_64
Vendor:         Norlook
Packager:       Andrei Ermilov (ioleeech@gmail.com)
Source0:        %{package_name}-%{package_version}.tar.gz
Provides:       norlook-toolchain-%{package_name}

BuildRequires:  norlook-toolchain-gmp
BuildRequires:  norlook-toolchain-mpfr
BuildRequires:  gcc

Requires:       norlook-toolchain-gmp
Requires:       norlook-toolchain-mpfr

# ----------------------------------------------------------------------------
# Sources preparing stage
# ----------------------------------------------------------------------------
%prep
# Cleanup building directory
rm -fr _build_
mkdir -pv _build_

# Cleanup sources and unpack tarball
rm -fr %{package_name}-%{package_version}
tar -xf %{_sourcedir}/%{package_name}-%{package_version}.tar.gz

# Apply patches
cd %{package_name}-%{package_version}
cd -

# ----------------------------------------------------------------------------
# Project building stage
# ----------------------------------------------------------------------------
%build
cd _build_

# Set environment variables
export CPPFLAGS="-I%{_norlook_toolchain}/include"
export CFLAGS="-O2 -I%{_norlook_toolchain}/include"
export CXXFLAGS="-O2 -I%{_norlook_toolchain}/include"
export LDFLAGS="-L%{_norlook_toolchain}/lib -Wl,-rpath,%{_norlook_toolchain}/lib"

# Configure the build
../%{package_name}-%{package_version}/configure \
  --prefix=%{_norlook_toolchain} \
  --with-gmp=%{_norlook_toolchain} \
  --with-mpfr=%{_norlook_toolchain} \
  --enable-shared \
  --disable-static \
  --disable-dependency-tracking

# Build
make %{?_smp_mflags}
cd -

# ----------------------------------------------------------------------------
# Checking stage
# ----------------------------------------------------------------------------
%check
cd _build_
make check
cd -

# ----------------------------------------------------------------------------
# Installation stage
# ----------------------------------------------------------------------------
%install
cd _build_
make install DESTDIR=%{buildroot}
rm -frv %{buildroot}/%{_norlook_toolchain}/share/
cd -

# ----------------------------------------------------------------------------
# RPM package description
# ----------------------------------------------------------------------------
%description
Norlook toolchain - GNU MPC package

%files
%defattr(-,root,root)
%{_norlook_toolchain}/*
