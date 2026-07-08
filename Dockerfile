FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY tarot-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY tarot-backend/ ./tarot-backend/
COPY tarot-frontend/ ./tarot-frontend/

WORKDIR /app/tarot-backend

# Hugging Face Spaces 使用 7860 端口
ENV PORT=7860

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
