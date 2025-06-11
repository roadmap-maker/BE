# 로드맵 프로젝트 백엔드 API

Django REST Framework와 Simple JWT를 사용한 로드맵 및 북마크 관리 API 서버입니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [기술 스택](#기술-스택)
- [환경 설정](#환경-설정)
- [설치 및 실행](#설치-및-실행)
- [API 문서](#api-문서)
- [프론트엔드 연동](#프론트엔드-연동)
- [문제 해결](#문제-해결)

## 🚀 프로젝트 개요

이 프로젝트는 사용자가 로드맵을 생성하고 관리할 수 있으며, 관심 있는 로드맵을 북마크할 수 있는 백엔드 API를 제공합니다.

### 주요 기능
- 사용자 인증 (회원가입, 로그인, JWT 토큰 관리)
- 로드맵 CRUD 작업
- 북마크 토글 기능 (PATCH 방식)
- CORS 설정으로 프론트엔드 연동 지원

## 🛠 기술 스택

- **Python**: 3.8+
- **Django**: 4.2.7
- **Django REST Framework**: 3.14.0
- **Simple JWT**: 5.3.0 (JWT 인증)
- **CORS Headers**: 4.3.1 (CORS 처리)
- **SQLite**: 기본 데이터베이스
- **python-dotenv**: 환경변수 관리

## ⚙️ 환경 설정

### 1. Python 설치 확인

먼저 Python이 설치되어 있는지 확인하세요:

```bash
python --version
# 또는
python3 --version
```

Python 3.8 이상이 필요합니다. 설치되어 있지 않다면 [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드하세요.

### 2. Git 클론 (이미 완료된 경우 생략)

```bash
git clone <repository-url>
cd BE
```

### 3. 가상환경 생성 및 활성화

**Windows:**
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate
```

가상환경이 활성화되면 터미널 프롬프트 앞에 `(venv)`가 표시됩니다.

## 📦 설치 및 실행

### 1. 의존성 설치 (pkg_resources 에러 방지)

```bash
# 1. 먼저 setuptools와 wheel 업그레이드
pip install --upgrade pip setuptools wheel

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 개발 모드로 프로젝트 설치 (권장)
pip install -e .
```

### 2. 환경변수 설정 (선택사항)

프로젝트 루트 디렉토리에 `.env` 파일을 생성하여 환경변수를 설정할 수 있습니다:

```bash
# .env 파일 생성
touch .env  # Windows에서는 파일 탐색기에서 직접 생성
```

`.env` 파일 내용 예시:
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=True
```

> **참고**: `.env` 파일이 없어도 기본값으로 실행됩니다.
> 그냥 예시 그대로 ㄱㄱ (어차피 돌아감)

### 3. 데이터베이스 마이그레이션

```bash
# 마이그레이션 파일 생성
python manage.py makemigrations

# 데이터베이스 적용
python manage.py migrate
```

### 5. 서버 실행

```bash
python manage.py runserver
```

서버가 성공적으로 실행되면 다음과 같은 메시지가 표시됩니다:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 주요 엔드포인트

- **인증**: `http://localhost:8000/auth/`
  - 회원가입: `POST /auth/signup`
  - 로그인: `POST /auth/login`
  - 토큰 갱신: `POST /auth/token/refresh`

- **로드맵**: `http://localhost:8000/roadmaps/`
  - 로드맵 목록: `GET /roadmaps`
  - 로드맵 생성: `POST /roadmaps`
  - 로드맵 상세: `GET /roadmaps/{id}`

- **북마크**: `http://localhost:8000/bookmarks/`
  - 북마크 토글: `PATCH /bookmarks/{roadmap_id}`

## 🌐 프론트엔드 연동

### CORS 설정

이 백엔드는 다음 프론트엔드 주소에서의 요청을 허용합니다:
- `http://localhost:3000` (React 기본 포트)
- `http://127.0.0.1:3000`

다른 포트를 사용하는 경우 `roadmap_project/settings.py`의 `CORS_ALLOWED_ORIGINS`를 수정하세요.

### 프론트엔드에서 API 호출 예시

**JavaScript/React 예시:**

```javascript
// 로그인
const login = async (username, password) => {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  return data;
};

// 인증이 필요한 API 호출
const fetchRoadmaps = async (accessToken) => {
  const response = await fetch('http://localhost:8000/roadmaps/', {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  });
  return response.json();
};

// 북마크 토글
const toggleBookmark = async (roadmapId, accessToken) => {
  const response = await fetch(`http://localhost:8000/bookmarks/${roadmapId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  });
  return response.json();
};
```

## 🛠️ 문제 해결

### 일반적인 문제들

1. **pkg_resources ModuleImportError**
   ```bash
   # setuptools 업그레이드
   pip install --upgrade setuptools wheel
   
   # 또는 가상환경 재생성
   deactivate
   rmdir /s venv  # Windows
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **포트 8000이 이미 사용 중인 경우**
   ```bash
   # 다른 포트 사용
   python manage.py runserver 8001
   ```

3. **CORS 에러가 발생하는 경우**
   - `settings.py`에서 `CORS_ALLOWED_ORIGINS` 확인
   - 프론트엔드 주소가 올바르게 설정되어 있는지 확인

4. **JWT 토큰 관련 에러**
   - `.env` 파일에 `JWT_SECRET_KEY` 설정 확인
   - 토큰 만료 시간 확인

5. **데이터베이스 관련 에러**
   ```bash
   # 마이그레이션 재실행
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **패키지 의존성 문제**
   ```bash
   # 개발 모드로 설치 (권장)
   pip install -e .
   
   # 또는 requirements.txt 재설치
   pip install -r requirements.txt --force-reinstall
   ```

### 로그 확인

서버 실행 중 오류가 발생하면 터미널에 표시되는 로그를 확인하세요. Django는 상세한 오류 정보를 제공합니다.

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해 주세요.

---

**Happy Coding! 🚀**