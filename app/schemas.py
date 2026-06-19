from pydantic import BaseModel

# Базовый класс с общими полями
class DinosaurBase(BaseModel):
    name: str 
    period: str | None = None
    length_min: float | None = None
    length_max: float | None = None
    weight_min: float | None = None
    weight_max: float | None = None
    image_url: str | None = None

# Для создания
class DinosaurCreate(DinosaurBase):
    pass

# Для обновления, все поля опциональны
class DinosaurUpdate(DinosaurBase):
    name: str | None = None
    period: str | None = None
    length_min: float | None = None
    length_max: float | None = None
    weight_min: float | None = None
    weight_max: float | None = None
    image_url: str | None = None

# Для ответа (есть id)
class DinosaurOut(DinosaurBase):
    id: int

    class Config:
        from_attributes = True