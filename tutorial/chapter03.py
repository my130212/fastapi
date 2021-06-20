from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date

from fastapi import APIRouter, Path, Query, Cookie, Header
from enum import Enum

app03 = APIRouter()

"""Path Parameters and Number Validations 路径参数和参数验证"""

#函数的顺序就是路由的顺序
@app03.get('/path/parameters')
def path_params01():
	return {"message": "This is my message"}

#路径参数
@app03.get('/path/{parameters}')
def path_params01(parameters: str):
	return {"message": parameters}


class CityName(str, Enum):
	Berjing = 'Bejing china'
	Shanghai = 'Shanghai china'

#枚举类型参数
@app03.get('/enum/{city}')
async def latest(city: CityName):
	if city == CityName.Berjing:
		return {'city': city, 'confirmed': 1400, 'death': 5}
	if city == CityName.Shanghai:
		return {'city': city, 'confirmed': 1500, 'death': 8}
	return {'city': city, "latest": 'unknown'}

#文件路径参数
@app03.get('/files/{files_path:path}')
def filepath(files_path: str):
	return f'The file path is {files_path}'

#路径参数的校验
@app03.get('/path/{num}')
def path_params_validata(num: int = Path('index', title='your number', description='不可描述',ge=1,le=10)):
	return num


"""Query Parameters and String Validations 查询参数和字符串的验证"""

@app03.get('/query')
def page_limit(page: int = 1,limit: Optional[int] = None):
	if limit:
		return {'page': page, 'limit': limit}
	return {'page': page}

@app03.get('/query/bool/conversion')
def type_conversion(param: bool = False):
	return param

#多个查询参数的列表，参数别名
@app03.get('/query/validations')
def query_params_validate(
		value: str = Query(...,min_length=8, max_length=16, regex='^a'),
		valueS: List[str] = Query(default=['vi','v2'], alias='alias_name')
):
	return value,valueS

"""Request Body and Fileds 请求体和字段"""

class CityInfo(BaseModel):
	name: str = Field(..., example="Beijing")
	country: str
	country_code: str = None
	country_population: int = Field(default=800, title='人口数量', description='国家的人口数量', ge=800)

	class Config:
		schema_extra = {
			"example": {
				"name": "shanghai",
				"country": "china",
				"country_code": "CN",
				"country_population": 1400000000
			}
		}

@app03.post("/request_body/city")
def city_info(city: CityInfo):
	print(city.name,city.country)
	return city.dict()

"""Request Body + Path parameter + Query parameter 多参数配合"""

#混合参数（路径参数、请求体、查询参数）
@app03.put("/request_body/city/{name}")
def mix_city_info(
		name: str,
		city01: CityInfo,
		city02: CityInfo,
		confirmed: int = Query(ge=0, description="确认数", default=0),
		death :int = Query(ge=0, description="死亡数", default=0)
):
	if name == "shanghai":
		return {"shanghai": {"confirmed": confirmed, "death": death}}
	return {name: city02.dict()}

"""Request Body - Nested Models 数据格式嵌套的请求体"""

class Data(BaseModel):
	city: List[CityInfo] = None #这里就是定义数据格式的请求体
	date: date
	confirmed: int = Field(ge=0, description="确认数", default=0)
	death : int = Field(ge=0, description="死亡数", default=0)
	recovered : int = Field(ge=0, description="痊愈书", default=0)

@app03.put("request_body/nested")
def nested_models(data: Data):
	return data

"""Cookie and Header 参数"""

@app03.get("/cookie")
def cookie(cookie_id: Optional[str] = Cookie(None)):
	return {"cookie_id": cookie_id}

@app03.get("/header")
def header(user_agent: Optional[str] = Header(None, convert_underscores=True), x_token: List[str] = Header(None)):
	"""
	有些HTTP代理和服务器是不允许在请求头中带有下划线的，所以Header提供convert_underscores属性设置
	:param user_agent: convert_underscores=True 会把user_agent变成 user-agent
	:param x_token:x_token包含多个值的列表
	:return
	"""
	return {"User-Agent": user_agent, "x-token": x_token}
