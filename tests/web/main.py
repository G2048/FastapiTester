from fastapi import FastAPI

from tests.web.models import CreateUser, GetUser

app = FastAPI()

counter = 0
USERS = {}


@app.post('/', response_model=GetUser)
async def create_user(user_model: CreateUser):
    global counter
    counter += 1
    user = GetUser(**user_model.dict(), id=counter)
    USERS[user.id] = user
    return user


@app.get('/')
async def list_users() -> dict:
    return USERS


@app.get('/{name}')
async def get_user_by_name(name: str) -> GetUser:
    for user in USERS.values():
        if user.name == name:
            return user


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
