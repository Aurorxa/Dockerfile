# JDK7 + Arthas Docker 镜像 (AlmaLinux 9)

这个 Docker 镜像基于 AlmaLinux 9，使用华为云的 JDK 7 RPM 包，集成了 Arthas 诊断工具，并自动执行 memory 命令来显示内存使用情况。

## 构建镜像

```bash
docker build -t jdk7-arthas .
```

## 运行容器

```bash
docker run -it --rm -p 3658:3658 -p 8563:8563 jdk7-arthas
```

## 功能说明

1. **基础镜像**: AlmaLinux 9
2. **JDK 版本**: Oracle JDK 7u80 (来自华为云镜像源)
3. **集成工具**: Arthas 诊断工具
4. **自动功能**: 
   - 移除系统默认的 JDK
   - 安装华为云的 JDK 7 RPM 包
   - 启动一个简单的 Java 测试应用程序
   - 自动连接 Arthas 到该应用程序
   - 执行 `memory` 命令显示内存使用情况

## JDK 详情

- **来源**: https://repo.huaweicloud.com/java/jdk/7u80-b15/jdk-7u80-linux-x64.rpm
- **版本**: JDK 7u80-b15
- **安装路径**: /usr/java/jdk1.7.0_80
- **环境变量**: JAVA_HOME 和 PATH 已正确配置

## 端口说明

- **3658**: Arthas Telnet 端口
- **8563**: Arthas HTTP 端口

## 使用方式

容器启动后会自动：
1. 编译并运行一个简单的 Java 应用程序
2. 获取应用程序的进程 ID (PID)
3. 使用 Arthas 连接到该 PID
4. 执行 `memory` 命令并输出结果

如果需要手动连接 Arthas，可以使用：
```bash
java -jar arthas-boot3.jar [PID]
```