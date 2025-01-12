FROM python:3.12-slim

# PostgreSQL 클라이언트 및 빌드 도구 설치
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . /app/

# Django 포트 노출
EXPOSE 8000

# 애플리케이션 시작 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
