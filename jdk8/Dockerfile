# 基于 AlmaLinux 9 的 JDK 8 + Arthas 4.x 内存分析镜像
FROM almalinux:9

# 设置环境变量
ENV APP_DIR=/app
ENV APP_HOME=${APP_DIR}
ENV ARTHAS_HOME=${APP_DIR}/arthas
ENV ARTHAS_VERSION=4.0.5
ENV PATH=${PATH}:${ARTHAS_HOME}/bin:/usr/local/bin

# 设置工作目录
WORKDIR ${APP_DIR}

# 安装必要的软件包和 JDK 8
RUN dnf update -y && \
    dnf install -y --allowerasing \
        java-1.8.0-openjdk \
        java-1.8.0-openjdk-devel \
        curl \
        wget \
        unzip \
        which \
        telnet \
    procps-ng \
        net-tools && \
    dnf clean all

# 设置 JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
ENV PATH=${JAVA_HOME}/bin:${PATH}

# 下载并安装 Arthas 4.x
RUN curl -L -o arthas-bin.zip \
    "https://github.com/alibaba/arthas/releases/download/arthas-all-${ARTHAS_VERSION}/arthas-bin.zip" && \
    unzip arthas-bin.zip -d ${APP_DIR}/ && \
    ls -la ${APP_DIR}/ && \
    mkdir -p ${ARTHAS_HOME} && \
    mv ${APP_DIR}/*.sh ${APP_DIR}/*.jar ${APP_DIR}/*.xml ${APP_DIR}/*.properties ${ARTHAS_HOME}/ 2>/dev/null || true && \
    mv ${APP_DIR}/lib ${APP_DIR}/async-profiler ${ARTHAS_HOME}/ 2>/dev/null || true && \
    rm -f arthas-bin.zip && \
    chmod +x ${ARTHAS_HOME}/*.sh && \
    ln -sf ${ARTHAS_HOME}/as.sh /usr/local/bin/as.sh

# 复制 Java 测试应用和启动脚本
COPY MemoryTestApp.java ${APP_DIR}/
COPY start.sh ${APP_DIR}/

# 编译 Java 应用并设置权限
RUN javac  -encoding UTF-8 MemoryTestApp.java && \
    chmod +x ${APP_DIR}/start.sh

# 验证安装
RUN echo "=== Installation Verification ===" && \
    java -version && \
    echo "Arthas location: ${ARTHAS_HOME}" && \
    ls -la ${ARTHAS_HOME}/ && \
    echo "Arthas version: ${ARTHAS_VERSION}"

# 暴露 Arthas 端口
EXPOSE 3658 8563

# 启动脚本
CMD ["./start.sh"]