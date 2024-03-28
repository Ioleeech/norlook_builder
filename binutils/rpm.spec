%define package_name     binutils
%define package_version  %{_version}
%define package_release  %{_release}

Summary:        Norlook toolchain - GNU Binutils package
Name:           norlook-toolchain-%{package_name}
Version:        %{package_version}
Release:        %{package_release}%{?dist}
Group:          Unspecified
License:        GPL-3.0
BuildArch:      x86_64
Vendor:         Norlook
Packager:       Andrei Ermilov (ioleeech@gmail.com)
Source0:        %{package_name}-%{package_version}.tar.xz
Patch0:         0001-sh-conf.patch
Patch1:         0002-poison-system-directories.patch
Provides:       norlook-toolchain-%{package_name}

BuildRequires:  gcc
BuildRequires:  texinfo
BuildRequires:  zlib-devel

# ----------------------------------------------------------------------------
# Sources preparing stage
# ----------------------------------------------------------------------------
%prep
# Cleanup building directory
rm -fr _build_
mkdir -pv _build_

# Cleanup sources and unpack tarball
rm -fr %{package_name}-%{package_version}
tar -xf %{_sourcedir}/%{package_name}-%{package_version}.tar.xz

# Apply patches
cd %{package_name}-%{package_version}
%patch0 -p 1
%patch1 -p 1
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
  --target=%{_norlook_target} \
  --disable-shared \
  --enable-static \
  --disable-doc \
  --disable-docs \
  --disable-documentation \
  --disable-debug \
  --disable-nls \
  --disable-dependency-tracking \
  --disable-multilib \
  --disable-plugins \
  --disable-werror \
  --disable-gprofng \
  --disable-sim \
  --disable-gdb \
  --enable-poison-system-directories \
  --enable-lto \
  --without-debuginfod \
  --without-zstd

# Build
make %{?_smp_mflags}
cd -

# ----------------------------------------------------------------------------
# Checking stage
# ----------------------------------------------------------------------------
%check
cd _build_
cd -

# ----------------------------------------------------------------------------
# Installation stage
# ----------------------------------------------------------------------------
%install
cd _build_
make                install DESTDIR=%{buildroot}
make -C ./bfd       install DESTDIR=%{buildroot}
make -C ./opcodes   install DESTDIR=%{buildroot}
make -C ./libiberty install DESTDIR=%{buildroot}
make -C ./libsframe install DESTDIR=%{buildroot}
rm -frv %{buildroot}/%{_norlook_toolchain}/share/
cd -

# ----------------------------------------------------------------------------
# RPM package description
# ----------------------------------------------------------------------------
%description
Norlook toolchain - GNU Binutils package

%files
%defattr(-,root,root)
/opt/norlook_toolchain/*
