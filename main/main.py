from fastapi import FastAPI, File, UploadFile, Response, HTTPException
from PIL import Image
from enum import Enum
import io
from typing import Optional
app = FastAPI()

class ImageFormat(str, Enum):
    png = "png"
    jpeg = "jpeg"
    jpg = "jpg"
    bmp = "bmp"
    gif = "gif"
    tiff = "tiff"
    webp = "webp"
    ico = "ico"
    ppm = "ppm"
    pgm = "pgm"
    pbm = "pbm"
    dds = "dds"
    eps = "eps"
    im = "im"
    pcx = "pcx"
    sgi = "sgi"
    tga = "tga"


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post('/resize-image')
async def upload_image(file: UploadFile = File(...), width: Optional[int] = None , height: Optional[int] = None, format: ImageFormat = ImageFormat.png):
    try:
        # Чтение и открытие изображения
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to open image: {str(e)}")
    
    # Если ширина и высота не были указаны, то просто возвращаем исходное изображение
    if width is None:
        width = image.width
    if height is None:
        height = image.height

    if width >= 1000000 or height >= 1000000:
        raise HTTPException(status_code=400, detail="Invalid dimensions provided for resizing")

    try:
        # Изменение размера изображения
        resized_image = image.resize((width, height))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid dimensions provided for resizing")

    
    try:
        # Сохранение изображения в указанный формат
        img_byte_arr = io.BytesIO()
        resized_image.save(img_byte_arr, format=format)
        img_byte_arr.seek(0)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid format provided for saving image")
    
    # Возврат изменённого изображения в ответе
    return Response(content=img_byte_arr.getvalue(), media_type=f"image/{format}")

    
