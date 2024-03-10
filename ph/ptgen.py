import re

import requests

from ph.common import prohibit, GroupMark
from util.log import logger


def fetch_and_format_ptgen_data(api_url, resource_url) -> (bool, str, dict):
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
                return False, "Pt-Gen请求失败，请检查网络连接", {}

    # 尝试解析JSON响应
    try:
        data = response.json()
    except ValueError:
        print("响应不是有效的JSON格式")
        return False, "Pt-Gen响应不是有效的JSON格式", {}

    # 根据响应获取中文名与英文名与年份
    chinese_name = data.get("chinese_title") if "chinese_title" in data else data.get("data", {}).get("chinese_title",
                                                                                                      "")
    trans_title = data.get("translated_title") if "translated_title" in data else data.get("data", {}).get(
        "translated_title", "")
    if trans_title != "":
        trans_title = trans_title[:1]
    year = data.get("year") if "year" in data else data.get("data", {}).get("year", "")
    # 类型
    category = data.get("genre") if "genre" in data else data.get("data", {}).get("genre", "")

    cast = data.get("cast") if "cast" in data else data.get("data", {}).get("cast", "")
    names = [item["name"].split()[0] for item in cast if not any(char.isdigit() for char in item["name"])]

    map = {
        "chinese_name": chinese_name,
        "trans_title": trans_title,
        "year": year,
        "category": category,
        "names": names
    }
    # 根据响应结构获取format字段
    format_data = data.get("format") if "format" in data else data.get("data", {}).get("format", "")
    if format_data == "":
        print("未找到format字段")
        return False, "Pt-Gen未找到format字段", map
    format_data += '\n'
    pattern = r"\[img\](.*?)\[/img\]"
    # 使用正则表达式进行替换
    result = re.sub(pattern, r"[img]\1[/img]" + GroupMark, format_data)
    return True, result, map
