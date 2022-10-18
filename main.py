from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class ModelName(str, Enum):
    # 만약 경로 매개변수를 받는 경로 동작이 있지만 유효하고 미리 정의할 수 있는 경로 매개변수 값을 원한다면 Enum을 사용할 수 있다.
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_price": item.price ,"item_id": item_id}

# 경로 동작을 만들때 고정 경로를 갖고 있는 상황이 생길 수 있다
# /users/me 현재 사용자의 데이터를 가져온다.
# /users/{user_id} 특정 사용자의 정보를 가져온다.
# 경로 동작은 순차적으로 평가되기 떄문에 /users/me 를 먼저 선언해주어야함
# 그렇지 않으면 /users/{user_id}는 매개변수 user_id의 값을 me라고 생각하게 된다.
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# 경로 변환기
# 매개변수에 path에 들어있는 값 자체가 필요할 때 ex) file_path = /home/johndoe/myfile.txt
# 매개변수가 / 를 가지고 있어서 / 로 시작해야 할 수 있음
# 이 경우 URL은 이중 슬래시 // 가 생김
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# 경로 매개변수의 읿부가 아닌 다른 함수 매개변수를 선언할 때
# 쿼리 매개변수로 자동 해석한다.
# 쿼리 매개변수는 고정된 부분이 아니므로 선택적일 수 있고 기본값을 가질 수 있음
# http://127.0.0.1:8000/items/ 로 이동하면
# http://127.0.0.1:8000/items/?skip=0&limit=10 와 같다.
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]