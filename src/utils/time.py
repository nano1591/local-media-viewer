from datetime import datetime
from typing import Optional
import pytz


def time_fmt(time: Optional[datetime] = None) -> str:
    # 如果没有传入时间，使用当前时间
    if time is None:
        time = datetime.now()

    # 设置中国时区
    china_tz = pytz.timezone("Asia/Shanghai")

    # 将时间转换为中国时区时间
    time_china = time.astimezone(china_tz)

    # 格式化时间为字符串，假设格式为：年-月-日 时:分:秒
    return time_china.strftime("%Y-%m-%d %H:%M:%S")
