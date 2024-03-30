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
  INSTALL_HDR_PATH="%{buildroot}/%{_norlook_toolchain}/%{_norlook_target}/sysroot/usr" \
  headers_install

# Remove ".install" and "..install.cmd" files
rm -fv $(find %{buildroot}/%{_norlook_toolchain}/%{_norlook_target}/sysroot/usr/ -name *.install*)

# ----------------------------------------------------------------------------
# RPM package description
# ----------------------------------------------------------------------------
%description
Norlook toolchain - Linux headers package

%files
%defattr(-,root,root)
%{_norlook_toolchain}/*
