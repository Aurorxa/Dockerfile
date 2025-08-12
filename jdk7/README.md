# JDK7 + Arthas Docker 镜像 (AlmaLinux 9)

这个 Docker 镜像基于 AlmaLinux 9，手动安装 JDK 7，集成了 Arthas 诊断工具，并自动执行 memory 命令来显示内存使用情况。

## 构建镜像

```bash
docker build -t jdk7-arthas . --no-cache --progress=plain
```

## 运行容器

```bash
# 一次性执行内存分析（推荐）
docker run --rm jdk7-arthas

```

## 功能特性

- **自动化内存分析**: 容器启动后自动执行内存分析并生成报告
- **一次性执行**: 完成分析后容器自动关闭，适合 CI/CD 集成
- **JDK 7 支持**: 使用华为云 JDK 7 RPM 包
- **Arthas 3.7.3**: 集成 Arthas 工具，支持 JDK 7
- **内存监控**: 自动执行 `memory` 命令显示内存使用情况
- **堆转储**: 自动生成堆转储文件用于深度分析
- **优雅关闭**: 支持信号处理，确保 Java 应用正常退出

## 执行流程

1. **启动 Java 应用**: 运行 `MemoryTestApp` 分配内存
2. **等待内存分配**: 等待 15 秒让应用分配足够内存
3. **执行 Arthas 分析**: 
   - 运行 `memory` 命令显示内存使用情况
   - 运行 `dashboard` 命令显示系统概览
   - 生成堆转储文件到 `/tmp/heapdump.hprof`
4. **优雅关闭**: 停止 Java 应用并退出容器

整个过程大约需要 30-60 秒完成。

## 功能说明

1. **基础镜像**: AlmaLinux 9
2. **JDK 版本**: Oracle JDK 7u80 (手动下载安装)
3. **集成工具**: Arthas 3.x 诊断工具
4. **自动功能**: 
   - 手动下载并安装 JDK 7u80
   - 解压并配置 arthas-bin.zip 中的工具
   - 启动一个简单的 Java 测试应用程序
   - 自动连接 Arthas 到该应用程序
   - 执行 `memory` 命令显示内存使用情况
   - 生成堆转储文件

## JDK 详情

- **来源**: https://repo.huaweicloud.com/java/jdk/7u80-b15/jdk-7u80-linux-x64.tar.gz
- **版本**: JDK 7u80-b15
- **安装路径**: /usr/local/jdk1.7.0_80 (符号链接: /usr/local/java)
- **环境变量**: JAVA_HOME 和 PATH 已正确配置

## Arthas 详情

- **版本**: 3.7.3
- **安装路径**: /app/arthas-bin/
- **主要脚本**: as3.sh (支持 JDK 7)
- **全局访问**: 已创建符号链接到 /usr/local/bin/as3.sh
- **支持命令**: memory, dashboard, heapdump 等

## 端口说明

- **3658**: Arthas Telnet 端口
- **8563**: Arthas HTTP 端口

## 使用方式

容器启动后会自动：
1. 编译并运行一个简单的 Java 应用程序
2. 获取应用程序的进程 ID (PID)
3. 使用 Arthas as3.sh 连接到该 PID
4. 执行 `memory` 命令并输出结果
5. 生成堆转储文件到 /tmp/heapdump.hprof

如果需要手动连接 Arthas，可以使用：
```bash
# 使用完整路径
/app/arthas-bin/as3.sh [PID]

# 或使用全局命令
as3.sh [PID]

# 执行特定命令
as3.sh [PID] -c "memory"
```

## 常用 Arthas 命令

- `memory` - 显示内存使用情况
- `dashboard` - 显示系统实时数据面板
- `heapdump` - 生成堆转储文件
- `jvm` - 显示 JVM 信息
- `thread` - 显示线程信息