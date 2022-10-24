from typing import Union
from fastapi import APIRouter, Body, FastAPI, Query, Path
from pydantic import BaseModel, Field
from enum import Enum

app = FastAPI()

# 엔드포인트를 한데 묶어서 관리
api = APIRouter(prefix="/api")
app.include_router(api)
class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(default=None, title="The description of the item", max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


class ModelName(str, Enum):
    # 만약 경로 매개변수를 받는 경로 동작이 있지만 유효하고 미리 정의할 수 있는 경로 매개변수 값을 원한다면 Enum을 사용할 수 있다.
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Query에 동일한 매개변수를 선언할 수 있다.
# title 메타데이터 값을 item_id에 선언할 때 아래와 같다.
# 경로 매개변수는 필수임으로 ...으로 필수임을 나타내는게 좋다.
# gt, ge, lt, le 검증 가능
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get", ge=1),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 단일 request body에는 키값을 생략하고 안의 데이터만 해석하도록 되어있음
# 키값을 부여하고 싶을 때 -> embed = True request body에 키값을 넣어줌
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = None,
    item: Item = Body(embed=True),
    user: User,
):
    results = {"item_id": item_id, "user": user}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

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
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]

# 생성한 모델로 매개변수처럼 선언
# 동작 원리
# 요청 본문을 JSON으로 읽음
# 해당 유형을 변환(필요할시)
# 데이터를 검증(유효핮 않으면 명확한 오류를 반환)
# 매개변수에 수신된 데이터를 제공
# OpenAPI 스키마의 일부이며 자동문서 UI에 적용된다.
@app.post("/items/")
async def create_item(item: Item):
    return item

# 쿼리 매개변수 및 문자열 유효성 검사
# q가 optional하고 길이가 50자 초과하지 않도록 강제
# 최소 길이: min_length
# 정규식: regex
# 기본값 default, ...으로 리터럴 값으로 설정 할 수 있음, pydantic의 Required으로도 가능함
# title, description 기능 제공
# alias 설정
# deprecated=True 사용되지 않음
# include_in_schema=False OpenAPI에서 제외
@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
        max_length=50,
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        alias="item-query",
        deprecated=True,
        include_in_schema=False,
        )
    ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results