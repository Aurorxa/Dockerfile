# 使用 Ubuntu 22.04 作为基础镜像，手动安装 JDK 7
FROM ubuntu:22.04

# 设置工作目录
WORKDIR /app

# 设置非交互模式
ENV DEBIAN_FRONTEND=noninteractive

# 安装必要的工具
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    unzip \
    procps \
    net-tools \
    telnet \
    ca-certificates \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 手动下载并安装 JDK 7
RUN wget -O jdk-7u80-linux-x64.tar.gz https://repo.huaweicloud.com/java/jdk/7u80-b15/jdk-7u80-linux-x64.tar.gz && \
    tar -xzf jdk-7u80-linux-x64.tar.gz -C /usr/local/ && \
    ln -s /usr/local/jdk1.7.0_80 /usr/local/java && \
    rm jdk-7u80-linux-x64.tar.gz

# 设置环境变量
ENV JAVA_HOME=/usr/local/java
ENV PATH=$PATH:$JAVA_HOME/bin:/opt/arthas

# 下载并安装 Arthas 3 (使用官方推荐方式)
RUN mkdir -p /opt/arthas && \
    wget -O /opt/arthas/arthas-boot.jar https://arthas.aliyun.com/arthas-boot3.jar && \
    chmod +x /opt/arthas/arthas-boot.jar

RUN java -version

# 创建一个示例 Java 应用程序
RUN echo 'import java.util.*;' > MemoryTestApp.java && \
    echo '' >> MemoryTestApp.java && \
    echo 'public class MemoryTestApp {' >> MemoryTestApp.java && \
    echo '    private static List<byte[]> memoryList = new ArrayList<>();' >> MemoryTestApp.java && \
    echo '    ' >> MemoryTestApp.java && \
    echo '    public static void main(String[] args) throws Exception {' >> MemoryTestApp.java && \
    echo '        System.out.println("Memory Test Application Started...");' >> MemoryTestApp.java && \
    echo '        System.out.println("PID: " + java.lang.management.ManagementFactory.getRuntimeMXBean().getName().split("@")[0]);' >> MemoryTestApp.java && \
    echo '        ' >> MemoryTestApp.java && \
    echo '        while(true) {' >> MemoryTestApp.java && \
    echo '            if(memoryList.size() < 100) {' >> MemoryTestApp.java && \
    echo '                memoryList.add(new byte[1024 * 1024]);' >> MemoryTestApp.java && \
    echo '                System.out.println("Allocated memory, total objects: " + memoryList.size());' >> MemoryTestApp.java && \
    echo '            }' >> MemoryTestApp.java && \
    echo '            Thread.sleep(5000);' >> MemoryTestApp.java && \
    echo '        }' >> MemoryTestApp.java && \
    echo '    }' >> MemoryTestApp.java && \
    echo '}' >> MemoryTestApp.java

# 编译 Java 应用
RUN $JAVA_HOME/bin/javac MemoryTestApp.java

# 创建启动脚本
RUN echo '#!/bin/bash \n\
    set -e \n\
    \n\
    echo "Starting Java application..." \n\
    java -Xmx512m -Xms256m MemoryTestApp & \n\
    APP_PID=$! \n\
    echo "Java application started with PID: $APP_PID" \n\
    \n\
    sleep 10 \n\
    \n\
    echo "Starting Arthas and executing memory command..." \n\
    \n\
    java -jar /opt/arthas/arthas-boot.jar $APP_PID --batch-mode -c "memory; quit" \n\
    \n\
    echo "Memory analysis completed. Keeping container running for inspection..." \n\
    \n\
    wait $APP_PID \n\
    ' > /app/start.sh

# 给脚本执行权限
RUN chmod +x /app/start.sh

# 暴露端口（Arthas web console 默认端口）
EXPOSE 3658 8563

# 启动命令
CMD ["./start.sh"]