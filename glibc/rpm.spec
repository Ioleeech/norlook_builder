%define package_name     glibc
%define package_version  %{_version}
%define package_release  %{_release}

Summary:        Norlook toolchain - The GNU C library package
Name:           norlook-toolchain-%{package_name}
Version:        %{package_version}
Release:        %{package_release}%{?dist}
Group:          Unspecified
License:        LGPL-2.0
BuildArch:      x86_64
Vendor:         Norlook
Packager:       Andrei Ermilov (ioleeech@gmail.com)
Source0:        %{package_name}-%{package_version}.tar.xz
Provides:       norlook-toolchain-%{package_name}

BuildRequires:  python3.11
BuildRequires:  norlook-toolchain-binutils
BuildRequires:  norlook-toolchain-gcc-initial
BuildRequires:  norlook-toolchain-linux-headers

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
cd -

# ----------------------------------------------------------------------------
# Project building stage
# ----------------------------------------------------------------------------
%build
cd _build_

# Set environment variables
export PATH="%{_norlook_toolchain}/bin/:${PATH}"

export CPP="%{_norlook_target}-cpp"
export CC="%{_norlook_target}-gcc"
export CXX="%{_norlook_target}-g++"
export LD="%{_norlook_target}-ld"

export CFLAGS="-O2 -fno-lto"
export CXXFLAGS="-O2 -fno-lto"

export libc_cv_forced_unwind=yes
export libc_cv_ssp=no

# Configure the build
../%{package_name}-%{package_version}/configure \
  --prefix=%{_norlook_toolchain}/%{_norlook_target} \
  --bindir=%{_norlook_toolchain}/%{_norlook_target}/bin \
  --sbindir=%{_norlook_toolchain}/%{_norlook_target}/bin \
  --libdir=%{_norlook_toolchain}/%{_norlook_target}/lib \
  --libexecdir=%{_norlook_toolchain}/%{_norlook_target}/lib \
  --includedir=%{_norlook_toolchain}/%{_norlook_target}/include \
  --oldincludedir=%{_norlook_toolchain}/%{_norlook_target}/include \
  --datarootdir=%{_norlook_toolchain}/%{_norlook_target}/share \
  --localstatedir=%{_norlook_toolchain}/%{_norlook_target}/var \
  --sysconfdir=%{_norlook_toolchain}/%{_norlook_target}/etc \
  --target=%{_norlook_target} \
  --host=%{_norlook_target} \
  --with-binutils=%{_norlook_toolchain}/%{_norlook_target}/bin \
  --with-headers=%{_norlook_toolchain}/%{_norlook_target}/include \
  --with-pkgversion=%{_norlook_version} \
  --with-bugurl=%{_norlook_url} \
  --without-gd \
  --enable-shared \
  --enable-static \
  --enable-crypt \
  --enable-kernel=%{_kernel_version} \
  --enable-lock-elision \
  --disable-profile \
  --disable-werror

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
export PATH="%{_norlook_toolchain}/bin/:${PATH}"
make install DESTDIR=%{buildroot}
rm -frv %{buildroot}/%{_norlook_toolchain}/%{_norlook_target}/share/info/
rm -frv %{buildroot}/%{_norlook_toolchain}/%{_norlook_target}/share/locale/
cd -

# ----------------------------------------------------------------------------
# RPM package description
# ----------------------------------------------------------------------------
%description
Norlook toolchain - The GNU C library package

%files
%defattr(-,root,root)
%{_norlook_toolchain}/*
