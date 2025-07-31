* 使用构建脚本

```bash
chmod +x build.sh && ./build.sh
```

* 直接命令
```
docker system prune -f
docker build -t fastapi-mock-service . && docker run -d -p 8000:8000 --name fastapi-mock-api fastapi-mock-service

```

* 访问：http://localhost:8000