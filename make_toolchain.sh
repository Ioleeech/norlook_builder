#!/usr/bin/env bash

# Path on the host where cross-platform compilling tools are placed
TOOLCHAIN_ROOT="/opt/norlook_toolchain"

# Arch of the host
TOOLCHAIN_ARCH="x86_64"

# Template of repo-file for repository with cross-platform compilling tools
TOOLCHAIN_REPO_FILE="norlook_builder.repo"

# Arch of the target
TOOLCHAIN_TARGET_ARCH="core2"
TOOLCHAIN_TARGET_NORMALIZED_ARCH="x86_64"

# Target name
TOOLCHAIN_TARGET="${TOOLCHAIN_TARGET_NORMALIZED_ARCH}-norlook-linux-gnu"

# Common variables for packages building
BUILDER_VER=$(date "+%Y%m%d%H%M%S")
BUILDER_DIST="$(/usr/bin/rpm --eval '%{dist}')"

BUILDER_ROOT=$(pwd)
BUILDER_TARBALLS="${BUILDER_ROOT}/_tarballs_"
BUILDER_REPO_DIR="${BUILDER_ROOT}/_repo_"
BUILDER_BUILD_DIR="${BUILDER_ROOT}/_build_"

# Package-specific parameters
PACKAGE_RPM_ROOT=""
PACKAGE_RPM_SPEC=""

# PACKAGE_VER is reserved for using with package.env files
# PACKAGE_URL is reserved for using with package.env files
# PACKAGE_SUM is reserved for using with package.env files

# Error message
CMD_ERROR=""

prepare_building_tree()
{
    local PACKAGE="$1"
    local PATCHES="${PACKAGE}/patches"
    local ENVFILE="${PACKAGE}/package.env"
    local SPECFILE="${PACKAGE}/rpm.spec"

    export PACKAGE_VER=
    export PACKAGE_URL=
    export PACKAGE_SUM=
    export $(grep -v '^#' ${ENVFILE} | xargs -d '\n')

    if [[ "X${PACKAGE_VER}" == "X" ]]; then
        CMD_ERROR="prepare_building_tree(): Bad \"${ENVFILE}\" file"
        exit -1
    fi

    PACKAGE_RPM_ROOT="${BUILDER_BUILD_DIR}/${PACKAGE}-${PACKAGE_VER}"
    PACKAGE_RPM_SPEC="${PACKAGE_RPM_ROOT}/SPECS/rpm.spec"

    echo ""
    echo "Preparing the building tree:"
    mkdir -pv ${BUILDER_TARBALLS}
    mkdir -pv ${BUILDER_BUILD_DIR}
    mkdir -pv ${BUILDER_REPO_DIR}/${TOOLCHAIN_ARCH}
    mkdir -pv ${PACKAGE_RPM_ROOT}/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

    echo ""
    echo "Updating the repository:"
    createrepo "${BUILDER_REPO_DIR}"

    local BUILDER_REPO_FILE="builder/${TOOLCHAIN_REPO_FILE}"
    local YUM_DNF_REPO_FILE="/etc/yum.repos.d/${TOOLCHAIN_REPO_FILE}"

    cp -fv "${BUILDER_REPO_FILE}" "${YUM_DNF_REPO_FILE}"
    sed -i "s!baseurl=.*!baseurl=file://${BUILDER_REPO_DIR}/!" "${YUM_DNF_REPO_FILE}"

    dnf update -y
    yum update -y

    echo ""
    echo "Getting the spec file:"
    cp -fv "${SPECFILE}" "${PACKAGE_RPM_SPEC}"

    if [[ -d "${PATCHES}" ]]; then
        echo ""
        echo "Getting patches:"
        cp -fv "${PATCHES}"/* "${PACKAGE_RPM_ROOT}/SOURCES/"
    fi
}

download_tarball()
{
    if [[ "X${PACKAGE_URL}"      == "X" ]] \
    || [[ "X${PACKAGE_SUM}"      == "X" ]] \
    || [[ "X${PACKAGE_RPM_ROOT}" == "X" ]]; then
        CMD_ERROR="download_tarball(): Bad initialization"
        exit -1
    fi

    local PACKAGE_FILE="${PACKAGE_URL##*/}"
    local TARBALL_PATH="${BUILDER_TARBALLS}/${PACKAGE_FILE}"
    local SOURCES_PATH="${PACKAGE_RPM_ROOT}/SOURCES/${PACKAGE_FILE}"

    if [[ -f "${TARBALL_PATH}" ]]; then
        echo ""
        echo "The tarball with sources is already downloaded:"
        echo "${TARBALL_PATH}"
    else
        echo ""
        echo "Downloading the tarball file with sources:"
        wget -P "${BUILDER_TARBALLS}/" "${PACKAGE_URL}"
    fi

    local PACKAGE_SHA512=$(sha512sum -b "${TARBALL_PATH}" | awk '{print $1}')

    # echo "PACKAGE_VER    = ${PACKAGE_VER}"
    # echo "PACKAGE_URL    = ${PACKAGE_URL}"
    # echo "PACKAGE_FILE   = ${PACKAGE_FILE}"
    # echo "TARBALL_PATH   = ${TARBALL_PATH}"
    # echo "SOURCES_PATH   = ${SOURCES_PATH}"
    # echo "PACKAGE_SUM    = ${PACKAGE_SUM}"
    # echo "PACKAGE_SHA512 = ${PACKAGE_SHA512}"

    if [[ "X${PACKAGE_SUM}" != "X${PACKAGE_SHA512}" ]]; then
        CMD_ERROR="download_tarball(): Bad checksum"
        exit -1
    fi

    cp -fv "${TARBALL_PATH}" "${SOURCES_PATH}"
}

install_dependencies()
{
    if [[ "X${PACKAGE_RPM_SPEC}" == "X" ]]; then
        CMD_ERROR="install_dependencies(): Bad initialization"
        exit -1
    fi

    local SPECFILE="${PACKAGE_RPM_SPEC}"
    local SPECPATH="$(dirname "${SPECFILE}")"
    local SPECDIR="$(readlink -f "${SPECPATH}")"

    local CMD_RUNNER=""
    if [[ $EUID -ne 0 ]]; then
        CMD_RUNNER="sudo"
    fi

    # To include all *.inc files correctly, the macro _specdir will be redefined
    local YUM_BUILD_OPT="--define='_specdir ${SPECDIR}'"

    echo ""
    echo "Installing dependencies:"

    ${CMD_RUNNER} yum-builddep -y "${YUM_BUILD_OPT}" "${SPECFILE}"
}

build_package()
{
    local PACKAGE="$1"

    prepare_building_tree "${PACKAGE}"
    download_tarball
    install_dependencies

    if [[ "X${PACKAGE_VER}"      == "X" ]] \
    || [[ "X${PACKAGE_RPM_SPEC}" == "X" ]] \
    || [[ "X${PACKAGE_RPM_ROOT}" == "X" ]]; then
        CMD_ERROR="build_package(): Bad initialization"
    fi

    if [[ "X${CMD_ERROR}" != "X" ]]; then
        echo "${CMD_ERROR}"
        exit -1
    fi

    echo ""
    echo "Building the package:"

    rpmbuild --verbose \
             --define "_topdir ${PACKAGE_RPM_ROOT}" \
             --define "_version ${PACKAGE_VER}" \
             --define "_release ${BUILDER_VER}" \
             --define "_norlook_toolchain ${TOOLCHAIN_ROOT}" \
             --define "_norlook_target ${TOOLCHAIN_TARGET}" \
             --define "_norlook_arch ${TOOLCHAIN_TARGET_ARCH}" \
             --define "_kernel_arch ${TOOLCHAIN_TARGET_NORMALIZED_ARCH}" \
             -bb "${PACKAGE_RPM_SPEC}"

    mv -fv "${PACKAGE_RPM_ROOT}/RPMS/${TOOLCHAIN_ARCH}"/*.rpm "${BUILDER_REPO_DIR}/${TOOLCHAIN_ARCH}/"
    createrepo "${BUILDER_REPO_DIR}"
}

build_package "binutils"
build_package "libgmp"
build_package "libmpfr"
build_package "libmpc"
build_package "gcc-initial"
build_package "linux-headers"
