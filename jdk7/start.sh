#!/bin/bash
set -e

# 使用环境变量获取路径
ARTHAS_SCRIPT="${ARTHAS_HOME}/as3.sh"

# 信号处理函数
cleanup() {
    echo ""
    echo "=== Received shutdown signal, cleaning up... ==="
    if [ ! -z "$APP_PID" ] && kill -0 $APP_PID 2>/dev/null; then
        echo "Stopping Java application (PID: $APP_PID)..."
        kill -TERM $APP_PID
        # 等待进程优雅退出
        for i in {1..10}; do
            if ! kill -0 $APP_PID 2>/dev/null; then
                echo "Java application stopped gracefully"
                break
            fi
            sleep 1
        done
        # 如果进程仍在运行，强制终止
        if kill -0 $APP_PID 2>/dev/null; then
            echo "Force killing Java application..."
            kill -KILL $APP_PID
        fi
    fi
    echo "Container shutdown complete"
    exit 0
}

# 捕获 SIGINT (Ctrl+C) 和 SIGTERM 信号
trap cleanup SIGINT SIGTERM

echo "=== AlmaLinux 9 + JDK 7 + Arthas 3 Memory Test ==="
echo "OS Info: $(cat /etc/os-release | grep PRETTY_NAME)"
echo "Java Version: $(java -version 2>&1 | head -1)"
echo "Arthas Location: ${ARTHAS_SCRIPT}"
echo "Press Ctrl+C to stop the container gracefully"

echo "Starting Java application..."
java -Xmx512m -Xms256m MemoryTestApp &
APP_PID=$!
echo "Java application started with PID: $APP_PID"

echo "Waiting for application to allocate some memory..."
sleep 15

echo "=== Starting Arthas Memory Analysis ==="
echo "Using Arthas from: ${ARTHAS_SCRIPT}"
${ARTHAS_SCRIPT} $APP_PID --batch-mode --use-http -c "memory; dashboard -n 1; heapdump /tmp/heapdump.hprof; quit"

echo "=== Memory Analysis Completed ==="
echo "Heap dump saved to /tmp/heapdump.hprof"
ls -lh /tmp/heapdump.hprof 2>/dev/null || echo "Heap dump not created"

echo "Keeping container running for inspection..."
echo "You can attach to this container and run more Arthas commands manually"
echo "Example: ${ARTHAS_SCRIPT} $APP_PID --use-http"
echo "Or use global command: as3.sh $APP_PID --use-http"
echo "Press Ctrl+C to stop the container"

# 使用 wait 等待子进程，这样可以正确处理信号
wait $APP_PID