from pydantic import BaseModel, Field

# Базовый класс с общими полями
class DinosaurBase(BaseModel):
    period: str | None = None
    length_min: float | None = None
    length_max: float | None = None
    weight_min: float | None = None
    weight_max: float | None = None
    image_url: str | None = None
    latin_name: str | None = None
    diet: str | None = None
    description: str | None = None

# Для создания
class DinosaurCreate(DinosaurBase):
    name: str = Field(..., min_length=1, description="Имя обязательно")
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
    latin_name: str | None = None
    diet: str | None = None
    description: str | None = None

# Для ответа (есть id)
class DinosaurOut(DinosaurBase):
    id: int
    name: str

    class Config:
        from_attributes = True