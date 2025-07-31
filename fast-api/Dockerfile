FROM almalinux:9

# 最小化安装
RUN dnf update -y && \
  dnf install -y python3 python3-devel gcc && \
  dnf clean all

# 安装 pip
RUN python3 -m ensurepip --upgrade

WORKDIR /app
COPY requirements.txt main.py ./
RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]