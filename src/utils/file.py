from datetime import datetime, timedelta
from typing import List, Union, Dict
import glob
import os
from pathlib import Path
from .cli import run_cli_command_async
import hashlib


# 使用glob查找指定目录下所有的m3u8和mp4文件
def get_video_files(
    static_directory: Union[str, Path], suffixs: List[str]
) -> List[str]:
    # 使用glob的递归模式查找所有m3u8和mp4文件
    # 获取符合条件的文件列表
    video_files = []
    for suffix in suffixs:
        pattern_suffix = os.path.join(static_directory, "**", f"*.{suffix}")
        video_files.extend(glob.glob(pattern_suffix, recursive=True))

        pattern_suffix = os.path.join(static_directory, "**", f"*.{suffix.upper()}")
        video_files.extend(glob.glob(pattern_suffix, recursive=True))

        pattern_suffix = os.path.join(static_directory, "**", f"*.{suffix.lower()}")
        video_files.extend(glob.glob(pattern_suffix, recursive=True))

    # 去重
    return list(set(video_files))


async def get_cover_jpeg_path(
    media_file: Union[str, Path], static_directory: Union[str, Path]
) -> str:
    media_file = Path(media_file)
    static_directory = Path(static_directory)

    # 确保封面图片文件夹存在
    cover_dir = static_directory / ".metadata"
    cover_dir.mkdir(parents=True, exist_ok=True)

    # 生成封面路径
    cover_path = cover_dir / (media_file.stem + ".jpeg")

    # 如果封面文件不存在，使用ffmpeg生成封面
    if not cover_path.exists():
        command = [
            "ffmpeg",
            "-i",
            str(media_file),
            "-vframes",
            "1",
            "-q:v",
            "2",  # 图片质量
            str(cover_path),
        ]
        result = await run_cli_command_async(command, timeout=60)
        if result["status"] != 0:
            raise Exception(f"Failed to generate cover for {media_file}")

    return str(cover_path)


def get_meta_config_path(static_directory: Union[str, Path]):
    static_directory = Path(static_directory)

    # 确保封面图片文件夹存在
    meta_dir = static_directory / ".metadata"
    meta_dir.mkdir(parents=True, exist_ok=True)

    meta_config_path = meta_dir / "meta_config.yaml"

    return str(meta_config_path)


def get_media_type(media_file: Union[str, Path]) -> str:
    """
    判断给定文件是 MP4 还是 M3U8 文件。

    :param media_file: 文件路径，支持字符串和 Path 类型。
    :return: 返回 "mp4" 或 "m3u8"。
    """
    media_file = Path(media_file)

    # 判断文件扩展名
    if media_file.suffix.lower() == ".mp4":
        return "mp4"
    elif media_file.suffix.lower() == ".m3u8":
        return "m3u8"
    else:
        return ""


async def get_media_metadata(
    media_file: Union[str, Path],
    static_directory: Union[str, Path],
    midia_name_block_strs: List[str],
) -> Dict:
    media_file = Path(media_file)
    static_directory = Path(static_directory)

    # 使用 get_cover_jpeg_path 函数获取封面路径
    cover_path = await get_cover_jpeg_path(media_file, static_directory)
    cover_url = f"/media/{Path(cover_path).relative_to(static_directory)}".replace(
        "\\", "/"
    )

    # 获取媒体信息
    media_url = f"/media/{media_file.relative_to(static_directory)}".replace("\\", "/")
    title = media_file.stem  # 默认使用文件名作为标题
    for block_str in midia_name_block_strs:
        title = title.replace(block_str, "")

    tags = [
        tag for tag in title.split() if tag != "-" and len(tag) <= 15
    ]  # 假设title是以空格分隔的多个标签

    # 获取视频总时长（秒）
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(media_file),
    ]
    result = await run_cli_command_async(command, timeout=60)
    if result["status"] == 0:
        total_duration = int(float(result["stdout"]))
    else:
        total_duration = 0

    # 获取文件信息，例如更新的时间戳
    update_timestamp = int(os.path.getmtime(media_file))

    return {
        "id": hashlib.sha256(media_url.encode()).hexdigest()[:10],
        "filename": media_file.name,
        "update_timestamp": update_timestamp,
        "media_time": str(timedelta(seconds=total_duration)),
        "media_url": media_url,
        "media_type": get_media_type(media_file),
        "cover_url": cover_url,
        "title": title,
        "tags": tags,
    }
