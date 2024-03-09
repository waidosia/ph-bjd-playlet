import re

import requests

from ph.common import prohibit, GroupMark
from util.log import logger


def fetch_and_format_ptgen_data(api_url, resource_url) -> (bool, str):
    response = None
    retry_count = 0
    while retry_count < 3:
        try:
            # 设置一个合理的超时时间，例如10秒
            response = requests.get(f"{api_url}?url={resource_url}", timeout=10)
            print(response.status_code)
            if response.status_code == 200:
                break
            if response is None:
                print("Pt-Gen请求失败")
                logger.error("Pt-Gen请求失败")
        except Exception as e:
            retry_count += 1
            if retry_count < 3:
                logger.info(f'进行第{retry_count}次重试，错误原因:{e}')
            else:
                logger.error(f'重试次数已用完')
                return False, "Pt-Gen请求失败，请检查网络连接"

    # 尝试解析JSON响应
    try:
        data = response.json()
    except ValueError:
        print("响应不是有效的JSON格式")
        return False, "Pt-Gen响应不是有效的JSON格式"

    # 根据响应结构获取format字段
    format_data = data.get("format") if "format" in data else data.get("data", {}).get("format", "")
    if format_data == "":
        print("未找到format字段")
        return False, "Pt-Gen未找到format字段"
    format_data += '\n'
    pattern = r"\[img\](.*?)\[/img\]"
    # 使用正则表达式进行替换
    result = re.sub(pattern, r"[img]\1[/img]" + GroupMark, format_data)
    return True, result
