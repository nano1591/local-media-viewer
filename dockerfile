# 使用轻量级 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 避免生成 .pyc 文件，强制 stdout/stderr 直接输出日志
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装依赖 (系统依赖 + python依赖)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件（如果有 requirements.txt / poetry.lock）
RUN pip install uv
COPY ./pyproject.toml ./uv.lock .
RUN uv sync

# 复制项目文件到容器
COPY . .

# 默认使用 uvicorn 启动 FastAPI
# 假设入口文件是 main.py，里面有 app 对象
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "critical"]
