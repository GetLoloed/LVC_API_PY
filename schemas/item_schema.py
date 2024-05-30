from pydantic import BaseModel


class ItemSchema(BaseModel):
    name: str
    description: str = None
    price: float
    is_available: bool = True

    class Config:
        from_attributes = True
