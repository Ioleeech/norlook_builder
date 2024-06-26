%define package_name     linux
%define package_version  %{_version}
%define package_release  %{_release}

Summary:        Norlook toolchain - Linux headers package
Name:           norlook-toolchain-%{package_name}-headers
Version:        %{package_version}
Release:        %{package_release}%{?dist}
Group:          Unspecified
License:        GPL-2.0
BuildArch:      x86_64
Vendor:         Norlook
Packager:       Andrei Ermilov (ioleeech@gmail.com)
Source0:        %{package_name}-%{package_version}.tar.xz
Provides:       norlook-toolchain-%{package_name}-headers

BuildRequires:  gcc

# ----------------------------------------------------------------------------
# Sources preparing stage
# ----------------------------------------------------------------------------
%prep
# Check the version
export SRC_VERSION="%{package_version}"
export SRC_VERSION_1="${SRC_VERSION%.*}"
export SRC_VERSION_2="${SRC_VERSION#*.}"

export SRC_MAJOR="${SRC_VERSION_1%.*}"
export SRC_MIDDLE="${SRC_VERSION_1#*.}"
export SRC_MINOR="${SRC_VERSION_2#*.}"

[[ "X${SRC_MAJOR}.${SRC_MIDDLE}" != "X%{_kernel_version}" ]] && \
  echo "Norlook builder requires linux kernel version %{_kernel_version}" && \
  echo "But %{package_name} package provides version %{package_version}" && \
  false

# Cleanup sources and unpack tarball
rm -fr %{package_name}-%{package_version}
tar -xf %{_sourcedir}/%{package_name}-%{package_version}.tar.xz

# Apply patches
cd %{package_name}-%{package_version}
cd -

# ----------------------------------------------------------------------------
# Project building stage
# ----------------------------------------------------------------------------
%build
# Do nothing
true

# ----------------------------------------------------------------------------
# Checking stage
# ----------------------------------------------------------------------------
%check
# Do nothing
true

# ----------------------------------------------------------------------------
# Installation stage
# ----------------------------------------------------------------------------
%install
# Install headers
make -C %{package_name}-%{package_version} \
  ARCH="%{_kernel_arch}" \
  INSTALL_HDR_PATH="%{buildroot}/%{_norlook_toolchain}/%{_norlook_target}/" \
  headers_install

# Remove ".install" and "..install.cmd" files
rm -fv $(find %{buildroot}/%{_norlook_toolchain}/%{_norlook_target}/ -name *.install*)

# ----------------------------------------------------------------------------
# RPM package description
# ----------------------------------------------------------------------------
%description
Norlook toolchain - Linux headers package

%files
%defattr(-,root,root)
%{_norlook_toolchain}/*
