from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, engine, Base
from app.models import Dinosaur
from app.schemas import DinosaurOut, DinosaurCreate, DinosaurUpdate
from typing import List
from sqlalchemy import text
from contextlib import asynccontextmanager
import os
import aiofiles
from pathlib import Path
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # Создаем таблицы
        await conn.run_sync(Base.metadata.create_all)
        # Активируем расширение
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
    yield

app = FastAPI(title="Dinosaurs API", lifespan=lifespan)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # разрешить все источники
    allow_credentials=True,
    allow_methods=["*"],  # разрешить все методы (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],
)

app.mount("/static/images", StaticFiles(directory="static/images"), name="images")

# Главная страница
@app.get("/")
async def root():
    html_path = os.path.join("app", "templates", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/ping")
async def ping():
    return {"status": "ok"}

# Поиск по имени (частичное совпадение)
@app.get("/dinosaurs/search")
async def search_dinosaur(
    db: AsyncSession = Depends(get_db),
    search: str | None = None,
    period: str | None = None,
    limit: int = 10,
    offset: int = 0
    ):
    
    query = """SELECT id, name, period, length_min, length_max, weight_min, weight_max, 
    image_url, latin_name, diet, description, created_at, updated_at FROM dinosaurs WHERE 1=1"""
    params = {}
    
    if search:
        query += " AND name ILIKE :search"
        params["search"] = f"%{search}%"

    if period:
        query += " AND period ILIKE :period"
        params["period"] = f"%{period}%"

    if search:
        query += " ORDER BY similarity(name, :search_sim) DESC"
        params["search_sim"] = search
    
    query += " LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    result = await db.execute(text(query), params)
    rows = result.fetchall()
    return [
    {
        "id": row[0],
        "name": row[1],
        "period": row[2],
        "length_min": row[3],
        "length_max": row[4],
        "weight_min": row[5],
        "weight_max": row[6],
        "image_url": row[7],
        "latin_name": row[8],
        "diet": row[9],
        "description": row[10]
    }
    for row in rows
    ]

# Фильтрация по Периоду
@app.get("/dinosaurs/filter")
async def filter_dinosaurs(
    db: AsyncSession = Depends(get_db),
    period: str | None = None,
    length_from: float | None = None,
    length_to: float | None = None,
    weight_from: float | None = None,
    weight_to: float | None = None,
    limit: int = 10,
    offset: int = 0
    ):

    query = """SELECT id, name, period, length_min, length_max, weight_min, weight_max, 
    image_url, latin_name, diet, description, created_at, updated_at FROM dinosaurs WHERE 1=1"""
    params = {}

    if period:
        query += " AND period ILIKE :period"
        params["period"] = f"%{period}%"

    if length_from is not None:
        query += " AND length_max >= :length_from"
        params["length_from"] = length_from
    
    if length_to is not None:
        query += " AND length_min <= :length_to"
        params["length_to"] = length_to
    
    if weight_from is not None:
        query += " AND weight_max >= :weight_from"
        params["weight_from"] = weight_from
    
    if weight_to is not None:
        query += " AND weight_min <= :weight_to"
        params["weight_to"] = weight_to

    query += " LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    result = await db.execute(text(query), params)
    rows = result.fetchall()
    return [
    {
        "id": row[0],
        "name": row[1],
        "period": row[2],
        "length_min": row[3],
        "length_max": row[4],
        "weight_min": row[5],
        "weight_max": row[6],
        "image_url": row[7],
        "latin_name": row[8],
        "diet": row[9],
        "description": row[10]
    }
    for row in rows
    ]

# Получить динозавра по id
@app.get("/dinosaurs/{id}")
async def get_dinosaur_by_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text
                              ("""SELECT id, name, period, length_min, length_max, weight_min, weight_max, 
                               image_url, latin_name, diet, description, created_at, updated_at 
                               FROM dinosaurs WHERE id = :id"""),
                              {"id": id}
                              )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Динозавр не найден")
    return {
        "id": row[0],
        "name": row[1],
        "period": row[2],
        "length_min": row[3],
        "length_max": row[4],
        "weight_min": row[5],
        "weight_max": row[6],
        "image_url": row[7],
        "latin_name": row[8],
        "diet": row[9],
        "description": row[10]
    }

# Получить всех динозавров с БД
@app.get("/dinosaurs", response_model=List[DinosaurOut])
async def get_all_dinosaurs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("""
        SELECT id, name, period, length_min, length_max, weight_min, weight_max, 
               image_url, latin_name, diet, description, created_at, updated_at
        FROM dinosaurs
    """))
    rows = result.fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "period": row[2],
            "length_min": row[3],
            "length_max": row[4],
            "weight_min": row[5],
            "weight_max": row[6],
            "image_url": row[7],
            "latin_name": row[8],
            "diet": row[9],
            "description": row[10]
        }
        for row in rows
    ]

# Добавить динозавра
@app.post("/dinosaurs", status_code=201)
async def create_dinosaur(
    dinosaur: DinosaurCreate,
    db: AsyncSession = Depends(get_db)
    ):
    new_dino = Dinosaur(
        name=dinosaur.name,
        period=dinosaur.period,
        length_min=dinosaur.length_min,
        length_max=dinosaur.length_max,
        weight_min=dinosaur.weight_min,
        weight_max=dinosaur.weight_max,
        image_url=dinosaur.image_url,
        latin_name=dinosaur.latin_name,
        diet=dinosaur.diet,
        description=dinosaur.description
    )
    db.add(new_dino)
    await db.commit()
    await db.refresh(new_dino)

    return new_dino

# Обноавить полностью данные о динозавре
@app.put("/dinosaurs/{id}")
async def put_dinosaur(id: int, dino_upd: DinosaurUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text
                              ("""SELECT id, name, period, length_min, length_max, weight_min, weight_max, 
                               image_url, latin_name, diet, description, created_at, updated_at 
                               FROM dinosaurs WHERE id = :id"""),
                              {"id": id}
                              )
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Динозавр не найден")

    update_data = dino_upd.model_dump(exclude_unset=True)

    if update_data:
        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = f"UPDATE dinosaurs SET {set_clause} WHERE id = :id"
        await db.execute(text(query), {**update_data, "id": id})
        await db.commit()

    result = await db.execute(text
                              ("""SELECT id, name, period, length_min, length_max, weight_min, weight_max, 
                               image_url, latin_name, diet, description, created_at, updated_at 
                               FROM dinosaurs WHERE id = :id"""),
                              {"id": id}
                              )
    rows = result.fetchone()
    return {
        {
        "id": row[0],
        "name": row[1],
        "period": row[2],
        "length_min": row[3],
        "length_max": row[4],
        "weight_min": row[5],
        "weight_max": row[6],
        "image_url": row[7],
        "latin_name": row[8],
        "diet": row[9],
        "description": row[10],
        "created_at": row[11],
        "updated_at": row[12]
        }
        for row in rows
    }
# Удалить динозавра
@app.delete("/dinosaurs/{id}")
async def delete_dinosaur(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text(
        "SELECT * FROM dinosaurs WHERE id = :id"),
        {"id": id}
    )
    row = result.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Динозавр не найден")
    
    await db.execute(text
                              ("""SELECT id, name, period, length_min, length_max, weight_min, weight_max, 
                               image_url, latin_name, diet, description, created_at, updated_at 
                               FROM dinosaurs WHERE id = :id"""),
                              {"id": id}
                              )
    await db.commit()

    return {
        "message": f"Динозавр с id {id} удален"
    }


# Загрузить изображение для динозавра
@app.post("/dinosaurs/{id}/image")
async def upload_dinosaur_image(
    id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
    ):
    
    result = await db.execute(text
                              ("""SELECT id, name, period, length_min, length_max, weight_min, weight_max, 
                               image_url, latin_name, diet, description, created_at, updated_at 
                               FROM dinosaurs WHERE id = :id"""),
                              {"id": id}
                              )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Динозавр не найден")
    
    old_image_url = row[7]
    if old_image_url:
        old_path = old_image_url.lstrip("/")
        if os.path.exists(old_path):
            os.remove(old_path)
            print(f"🗑️ Удалён старый файл: {old_path}")

    extension = Path(file.filename).suffix
    if not extension:
        extension = ".jpg"

    os.makedirs("static/images", exist_ok=True)

    file_path = f"static/images/dino_{id}{extension}"
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    image_url = f"/static/images/dino_{id}{extension}"
    await db.execute(text
                     ("UPDATE dinosaurs SET image_url = :image_url WHERE id = :id"),
                     {"image_url": image_url, "id": id}
                     )
    await db.commit()
    return {
        "message": "Изображение загружено", 
        "image_url": image_url
    }
