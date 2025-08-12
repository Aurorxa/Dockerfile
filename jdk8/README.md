# JDK 8 + Arthas 4.x Docker 镜像

基于 AlmaLinux 9 的 JDK 8 + Arthas 4.x 内存分析 Docker 镜像。

## 构建镜像

```bash
docker build -t jdk8-arthas .
```

## 运行容器

```bash
# 一次性执行内存分析（推荐）
docker run --rm jdk8-arthas

```

## 功能特性

- **自动化内存分析**: 容器启动后自动执行内存分析并生成报告
- **一次性执行**: 完成分析后容器自动关闭，适合 CI/CD 集成
- **JDK 8 支持**: 使用 AlmaLinux 9 官方 JDK 8 包
- **Arthas 4.x**: 集成最新版本 Arthas 4.0.5，支持 JDK 8+
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

## 技术规格

- **基础镜像**: AlmaLinux 9
- **JDK 版本**: OpenJDK 1.8.0
- **Arthas 版本**: 4.0.5 <mcreference link="https://arthas.aliyun.com/" index="3">3</mcreference>
- **安装路径**: `/app/arthas`
- **启动脚本**: `as.sh` (适用于 JDK 8+)
- **端口**: 3658 (Telnet), 8563 (HTTP)

## 环境变量

- `APP_DIR`: 应用目录 (默认: `/app`)
- `APP_HOME`: 应用主目录 (默认: `/app`)
- `ARTHAS_HOME`: Arthas 安装目录 (默认: `/app/arthas`)
- `ARTHAS_VERSION`: Arthas 版本 (默认: `4.0.5`)
- `JAVA_HOME`: JDK 安装目录

## 手动使用 Arthas

如果需要手动连接 Arthas，可以使用以下命令：

```bash
# 进入容器
docker exec -it <container_id> bash

# 连接到 Java 进程
as.sh <pid> --use-http

# 或使用全局命令
/app/arthas/as.sh <pid> --use-http
```

## 常用 Arthas 命令

- `memory`: 查看内存使用情况
- `dashboard`: 实时系统概览
- `thread`: 查看线程信息
- `jvm`: 查看 JVM 信息
- `gc`: 查看 GC 信息
- `heapdump`: 生成堆转储文件

## 与 JDK 7 版本的区别

| 特性 | JDK 7 版本 | JDK 8 版本 |
|------|------------|------------|
| JDK 版本 | JDK 7 (华为云) | OpenJDK 8 (官方) |
| Arthas 版本 | 3.7.3 | 4.0.5 |
| 启动脚本 | `as3.sh` | `as.sh` |
| 功能支持 | 基础功能 | 完整功能 + 新特性 |
| 性能 | 较低 | 更好 |

## 注意事项

1. **JDK 兼容性**: Arthas 4.x 不再支持 JDK 6/7 <mcreference link="https://github.com/alibaba/arthas" index="5">5</mcreference>
2. **内存要求**: 建议至少分配 512MB 堆内存
3. **端口映射**: 确保映射 3658 和 8563 端口用于远程访问
4. **容器生命周期**: 默认执行完成后自动退出