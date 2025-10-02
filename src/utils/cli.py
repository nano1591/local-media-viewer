import subprocess


def run_cli_command(command, timeout=60):
    """
    运行CLI命令并返回状态、标准输出、错误输出。

    :param command: 要执行的命令，作为列表形式（例如 ["python", "script.py"]）。
    :param timeout: 设置超时时间（秒）。
    :return: 字典，包含返回状态、标准输出、错误输出。
    """
    result = {"status": None, "stdout": None, "stderr": None}

    try:
        # 使用 subprocess.run 来执行命令
        # capture_output=True 表示捕获输出
        # text=True 表示返回字符串而非字节
        # timeout=timeout 设置超时时间
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,  # 防止非零状态码时抛出异常
        )

        result["status"] = process.returncode  # 获取返回的状态码
        result["stdout"] = process.stdout.strip()  # 获取标准输出
        result["stderr"] = process.stderr.strip()  # 获取错误输出

    except subprocess.TimeoutExpired as e:
        result["status"] = -1
        result["stderr"] = f"Timeout expired after {timeout} seconds"
    except subprocess.CalledProcessError as e:
        result["status"] = e.returncode
        result["stderr"] = e.stderr.strip()
    except Exception as e:
        result["status"] = -2
        result["stderr"] = str(e)

    return result


import asyncio


async def run_cli_command_async(command: list, timeout: int = 60) -> dict:
    """
    异步执行命令行命令并返回状态、标准输出和错误输出。

    :param command: 要执行的命令，作为列表形式（例如 ["python", "script.py"]）。
    :param timeout: 设置超时时间（秒）。
    :return: 字典，包含返回状态、标准输出和错误输出。
    """
    result = {"status": None, "stdout": None, "stderr": None}

    try:
        # 创建异步子进程
        process = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        # 使用 asyncio.wait_for() 来设置超时时间
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

        # 获取返回状态码
        result["status"] = process.returncode
        result["stdout"] = stdout.decode().strip()  # 标准输出
        result["stderr"] = stderr.decode().strip()  # 错误输出
    except asyncio.TimeoutError:
        result["status"] = -1
        result["stderr"] = f"Timeout expired after {timeout} seconds"
    except Exception as e:
        result["status"] = -2
        result["stderr"] = str(e)

    return result
