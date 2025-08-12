# 使用 AlmaLinux 9 作为基础镜像，手动安装 JDK 7
FROM almalinux:9

# 定义应用目录变量
ARG APP_DIR=/opt/jdk7-arthas
ENV APP_HOME=${APP_DIR}
ENV ARTHAS_HOME=${APP_HOME}/arthas-bin

# 设置工作目录
WORKDIR ${APP_HOME}

# 安装必要的工具和依赖
RUN dnf update -y && \
    dnf install -y \
    --allowerasing \
    wget \
    curl \
    unzip \
    procps-ng \
    net-tools \
    telnet \
    tree \
    ca-certificates \
    glibc.i686 \
    libgcc.i686 \
    && dnf clean all 

# 手动下载并安装 JDK 7
RUN wget -O jdk-7u80-linux-x64.tar.gz https://repo.huaweicloud.com/java/jdk/7u80-b15/jdk-7u80-linux-x64.tar.gz && \
    tar -xzf jdk-7u80-linux-x64.tar.gz -C /usr/local/ && \
    ln -s /usr/local/jdk1.7.0_80 /usr/local/java && \
    rm jdk-7u80-linux-x64.tar.gz

# 设置环境变量
ENV JAVA_HOME=/usr/local/java
ENV PATH=$PATH:$JAVA_HOME/bin:$ARTHAS_HOME

# 复制并安装 Arthas
COPY arthas-bin.zip .
RUN unzip arthas-bin.zip && \
    cd arthas-bin && \
    chmod +x *.sh && \
    # 创建符号链接，方便全局访问
    ln -sf ${ARTHAS_HOME}/as3.sh /usr/local/bin/as3.sh && \
    # 验证 arthas 文件
    ls -la ${ARTHAS_HOME}/ && \
    echo "Arthas installation completed"

# 验证 Java 安装
RUN java -version

# 复制并编译 Java 应用程序
COPY MemoryTestApp.java .
RUN $JAVA_HOME/bin/javac -encoding UTF-8 MemoryTestApp.java

# 复制并设置启动脚本
COPY start.sh .
RUN chmod +x ${APP_HOME}/start.sh

# 暴露端口（Arthas web console 默认端口）
EXPOSE 3658 8563

# 启动命令
CMD ["./start.sh"]