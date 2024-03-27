FROM rockylinux:8

RUN dnf update -y && \
    dnf install -y yum-utils createrepo && \
    yum-config-manager --enable powertools && \
    yum-config-manager --enable devel      && \
    dnf update -y && \
    yum update -y && \
    dnf install -y coreutils-single git wget rsync perl gcc gcc-c++ make cmake \
                   zlib-devel zlib-static gmp-devel gmp-static mpfr-devel libmpc-devel \
                   which bc m4 bison gettext texinfo gawk gawk-devel ncurses ncurses-devel \
                   rpm-build mc && \
    dnf clean all && rm -rf /var/cache/dnf && \
    yum clean all && rm -rf /var/cache/yum
