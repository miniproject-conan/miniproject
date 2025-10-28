###  .env 파일 안에 넣을 내용
```bash
PROJECT_NAME=Diary API

DATABASE_URL=postgres://conan:mynameisconan@localhost:5432/fastapi_db

PASSWORD_SALT=
JWT_SECRET_KEY=i_am_conan
JWT_ALGORITHM=HS256
JWT_ACCESS_MINUTES=60
JWT_REFRESH_DAYS=14

DEBUG_MODE=True # 여기는 배포할 때 False 해주쇼~
HOST=127.0.0.1
PORT=8000
```


<hr>

초기 설정 터미널 명령어
```
poetry run aerich init -t app.db.config.TORTOISE_ORM
poetry run aerich init-db
```
