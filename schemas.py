from pydantic import BaseModel


class Image(BaseModel):
	code: int
	name: str
	data: str
