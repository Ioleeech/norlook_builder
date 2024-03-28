%define package_name     gcc
%define package_version  %{_version}
%define package_release  %{_release}

Summary:        Norlook toolchain - GCC package (required to compile target C library only)
Name:           norlook-toolchain-%{package_name}-initial
Version:        %{package_version}
Release:        %{package_release}%{?dist}
Group:          Unspecified
License:        GPL-3.0
BuildArch:      x86_64
Vendor:         Norlook
Packager:       Andrei Ermilov (ioleeech@gmail.com)
Source0:        %{package_name}-%{package_version}.tar.xz
Patch0:         0001-disable-split-stack-for-non-thread-builds.patch
Patch1:         0002-or1k-Only-define-TARGET_HAVE_TLS-when-HAVE_AS_TLS.patch
Patch2:         0003-xtensa-add-.note.GNU-stack-section-on-linux.patch
Provides:       norlook-toolchain-%{package_name}-initial

BuildRequires:  norlook-toolchain-binutils
BuildRequires:  norlook-toolchain-gmp
BuildRequires:  norlook-toolchain-mpfr
BuildRequires:  norlook-toolchain-mpc
BuildRequires:  gcc

Requires:       norlook-toolchain-binutils
Requires:       norlook-toolchain-gmp
Requires:       norlook-toolchain-mpfr
Requires:       norlook-toolchain-mpc

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
%patch2 -p 1
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

export CFLAGS_FOR_TARGET="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -Ofast -D_FORTIFY_SOURCE=1"
export CXXFLAGS_FOR_TARGET="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 -Ofast -D_FORTIFY_SOURCE=1"

# Configure the build
../%{package_name}-%{package_version}/configure \
  --prefix=%{_norlook_toolchain} \
  --target=%{_norlook_target} \
  --with-arch=%{_norlook_arch} \
  --with-pkgversion=norlook \
  --with-bugurl=https://github.com/Ioleeech/norlook_builder \
  --with-gmp=%{_norlook_toolchain} \
  --with-mpfr=%{_norlook_toolchain} \
  --with-mpc=%{_norlook_toolchain} \
  --without-headers \
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
  --disable-threads \
  --disable-libatomic \
  --disable-libitm \
  --disable-libssp \
  --disable-decimal-float \
  --disable-largefile \
  --enable-lto \
  --enable-tls \
  --enable-libquadmath \
  --enable-libquadmath-support \
  --enable-languages=c \
  --enable-__cxa_atexit \
  --with-gnu-ld \
  --with-newlib \
  --without-isl \
  --without-cloog \
  --without-zstd

# Build
make %{?_smp_mflags} all-gcc
make %{?_smp_mflags} all-target-libgcc
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
make install-gcc DESTDIR=%{buildroot}
make install-target-libgcc DESTDIR=%{buildroot}
rm -frv %{buildroot}/%{_norlook_toolchain}/include/
rm -frv %{buildroot}/%{_norlook_toolchain}/share/
cd -

# ----------------------------------------------------------------------------
# RPM package description
# ----------------------------------------------------------------------------
%description
Norlook toolchain - GCC package (required to compile target C library only)

%files
%defattr(-,root,root)
/opt/norlook_toolchain/*
