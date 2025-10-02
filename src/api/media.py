from pathlib import Path
import traceback
import anyio
from fastapi import FastAPI, HTTPException
from ..utils.file import get_video_files, get_media_metadata, get_meta_config_path
from ..global_settings import GlobalSettings
from ..utils.time import time_fmt
import yaml
import os

media_app = FastAPI()
global_settings = GlobalSettings()


@media_app.post("/flush/metadata")
async def flush_metadata():
    try:
        files = get_video_files(
            static_directory=global_settings.media_dir_path,
            suffixs=global_settings.allow_midia_suffixs,
        )

        medias = []
        for file in files:
            metadata = await get_media_metadata(
                media_file=file,
                static_directory=global_settings.media_dir_path,
                midia_name_block_strs=global_settings.midia_name_block_strs,
            )
            medias.append(metadata)

        meta = {
            "timestamp": time_fmt(),
            "medias": sorted(
                medias,
                key=lambda x: x["update_timestamp"],
                reverse=True,
            ),
        }

        meta_config_path = get_meta_config_path(
            static_directory=global_settings.media_dir_path,
        )
        with open(meta_config_path, "w") as yaml_file:
            yaml.dump(
                meta,
                yaml_file,
                default_flow_style=False,
                allow_unicode=True,
                encoding="utf-8",
            )
        return {}

    except Exception as e:
        print(traceback.format_exc(), flush=True)
        raise HTTPException(500, str(e))


@media_app.get("/media/list")
async def get_media_list():
    try:
        meta_config_path = Path(
            get_meta_config_path(
                static_directory=global_settings.media_dir_path,
            )
        )
        if not meta_config_path.exists():
            return []

        async with await anyio.open_file(meta_config_path, "r") as f:
            yaml_str = await f.read()
            config = yaml.safe_load(yaml_str)
        return config["medias"]
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        raise HTTPException(500, str(e))


@media_app.get("/media/{id}")
async def get_media_detail(id: str):
    try:
        meta_config_path = Path(
            get_meta_config_path(
                static_directory=global_settings.media_dir_path,
            )
        )
        if not meta_config_path.exists():
            return {}

        async with await anyio.open_file(meta_config_path, "r") as f:
            yaml_str = await f.read()
            config = yaml.safe_load(yaml_str)

        for media in config["medias"]:
            if media["id"] == id:
                return media

        return {}
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        raise HTTPException(500, str(e))
