#!/bin/bash

# 1. 构建 Docker 镜像
echo "构建 Docker 镜像..."
docker build -t fastapi-mock-service:latest .

# 2. 运行容器
echo "启动容器..."
docker run -d \
    --name fastapi-mock-api \
    -p 8000:8000 \
    --restart unless-stopped \
    fastapi-mock-service:latest

# 3. 查看容器状态
echo "检查容器状态..."
docker ps -a | grep fastapi-mock-api

# 4. 查看容器日志
echo "查看容器日志..."
docker logs fastapi-mock-api

# 5. 测试API服务
echo "等待服务启动..."
sleep 5
echo "测试API服务..."
curl -s http://localhost:8000/health | python3 -m json.tool

echo ""
echo "=== 服务信息 ==="
echo "API服务地址: http://localhost:8000"
echo "API文档地址: http://localhost:8000/docs"
echo "健康检查: http://localhost:8000/health"
echo ""
echo "=== 常用命令 ==="
echo "查看日志: docker logs fastapi-mock-api"
echo "进入容器: docker exec -it fastapi-mock-api bash"
echo "停止容器: docker stop fastapi-mock-api"
echo "删除容器: docker rm fastapi-mock-api"
echo "删除镜像: docker rmi fastapi-mock-service:latest"