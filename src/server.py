from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .global_settings import GlobalSettings
from starlette.middleware.gzip import GZipMiddleware
from .api.media import media_app, get_media_list, get_media_detail
from fastapi.templating import Jinja2Templates

app = FastAPI()
settings = GlobalSettings()

# 添加GZip中间件
app.add_middleware(GZipMiddleware, minimum_size=1000)
# 将static文件夹挂载到"/static"路径下
app.mount("/static", StaticFiles(directory=Path("src/static")), name="static")
app.mount("/media", StaticFiles(directory=settings.media_dir_path), name="media")
app.mount("/api", media_app)

templates = Jinja2Templates(directory=Path("src/templates"))


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    media_list = await get_media_list()
    return templates.TemplateResponse(
        request=request,
        name="list.html",
        context={
            "list": media_list,
            "list_length": len(media_list),
            "lastClickId": request.query_params.get("lastClickId"),
        },
    )


@app.get("/item/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    item = await get_media_detail(id=id)
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id, "item": item}
    )
