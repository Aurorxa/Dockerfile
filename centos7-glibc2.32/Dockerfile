# 选择运行时基础镜像
FROM centos:7

# 安装依赖
RUN yum -y -q update && \
  yum -y -q install deltarpm bison python3 wget make xz epel-release  && \
  yum -y -q install bzip2 nss_test2 gettext texinfo binutils gdb && \
  yum -y -q install libmpc-devel mpfr-devel gmp-devel gcc gcc-c++ gcc-c++-devel zlib-devel gcc-gfortran.x86_64 zlib

# 环境变量
ENV MAKE_VERSION=4.3
ENV GCC_VERSION=9.5.0
ENV GLIBC_VERSION=2.32
ENV NVM_DIR=$HOME/.nvm
ENV NODE_VERSION=20.11.1  

# 升级 make
RUN cd $HOME && \
  # wget https://ftp.gnu.org/gnu/make/make-${MAKE_VERSION}.tar.gz && \
  wget -q https://mirrors.aliyun.com/gnu/make/make-${MAKE_VERSION}.tar.gz && \
  tar -xf make-${MAKE_VERSION}.tar.gz && \
  cd make-${MAKE_VERSION} && \
  mkdir build && cd build && \
  ../configure && \
  make -j$(nproc) -s && \
  make install && \
  ln -s -f /usr/local/bin/make /usr/bin/make && \
  make -v 

# 升级 gcc
RUN cd $HOME && \
  # wget https://ftp.gnu.org/gnu/gcc/gcc-7.3.0/gcc-7.3.0.tar.gz && \
  wget -q https://mirrors.aliyun.com/gnu/gcc/gcc-${GCC_VERSION}/gcc-${GCC_VERSION}.tar.gz && \
  tar -xf gcc-${GCC_VERSION}.tar.gz && \
  cd gcc-${GCC_VERSION} && \
  mkdir build && cd build && \
  ../configure --prefix=/usr --disable-multilib --enable-languages=c,c++,fortran  && \
  make -j$(nproc) -s && \
  yum -y -q remove gcc && \
  make install && \
  gcc -v

# 升级 glibc
RUN cd $HOME && \
  # wget https://ftp.gnu.org/gnu/glibc/glibc-${GLIBC_VERSION}.tar.gz && \
  wget -q https://mirrors.aliyun.com/gnu/glibc/glibc-${GLIBC_VERSION}.tar.gz && \
  tar -xf glibc-${GLIBC_VERSION}.tar.gz && \
  cd glibc-${GLIBC_VERSION}/ && \
  mkdir build  && cd build && \
  ../configure --prefix=/usr --disable-profile --enable-add-ons --with-headers=/usr/include --with-binutils=/usr/bin --disable-sanity-checks --disable-werror && \
  make -j$(nproc) -s && \
  sed -i '128i\        && $name ne "nss_test2"' ../scripts/test-installation.pl && \
  make install && \
  make localedata/install-locales && \
  strings /lib64/libc.so.6 | grep ^GLIBC_ && \
  ldd --version

# 安装 nvm
# RUN cd $HOME && \ 
#   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
#   source $HOME/.bashrc && \
#   nvm install $NODE_VERSION && \
#   nvm alias default $NODE_VERSION && \
#   npm install -g npm@latest

# ENV PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH  

# # # 验证安装结果
# RUN node -v && npm -v

# 清理缓存
RUN rm -f $HOME/glibc-${GLIBC_VERSION}.tar.gz && \
  rm -f $HOME/gcc-${GCC_VERSION}.tar.gz && \
  rm -f $HOME/make-${MAKE_VERSION}.tar.gz && \
  yum clean all && \
  rm -rf /var/cache/yum




