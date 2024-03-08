import json
import os

from pymediainfo import MediaInfo

from util.log import logger


def get_video_info(file_path):
    logger.info("开始获取视频信息,用于输出长宽比")
    if not os.path.exists(file_path):
        logger.error("文件路径不存在")
        print("文件路径不存在")
        return False, ["视频文件路径不存在"]
    try:
        media_info = MediaInfo.parse(file_path)
        width, _, hdr_format, commercial_name, channel_layout = extract_video_info(media_info)
        logger.info(f"获取视频信息成功: {width}, {hdr_format}, {commercial_name}, {channel_layout}")
        return True, [get_abbreviation(width), get_abbreviation(_), get_abbreviation(hdr_format),
                      get_abbreviation(commercial_name), get_abbreviation(channel_layout)]
    except OSError as e:
        # 文件路径相关的错误
        logger.error(f"文件路径错误: {e}")
        print(f"文件路径错误: {e}")
        return False, [f"文件路径错误: {e}"]
    except Exception as e:
        # MediaInfo无法解析文件
        logger.error(f"无法解析文件: {e}")
        print(f"无法解析文件: {e}")
        return False, [f"无法解析文件: {e}"]


def extract_video_info(media_info):
    width = ""
    _ = ""
    hdr_format = ""
    commercial_name = ""
    channel_layout = ""

    # 需判断视频为横屏还是竖排

    for track in media_info.tracks:
        if track.track_type == "Video":
            if track.other_width:
                width = track.other_width[0]  # 短剧 720  2560
                high = track.other_height[0]  # 短剧 1280  1072
                w = str(width).replace("pixels", "").replace(" ", "")
                h = str(high).replace("pixels", "").replace(" ", "")
                if int(w) > int(h):
                    width, high = high, width
            if track.other_format:
                _ = track.other_format[0]
            if track.other_hdr_format:
                hdr_format = track.other_hdr_format[0]
        elif track.track_type == "Audio":
            commercial_name = track.format
            channel_layout = track.channel_layout
            break
        else:
            continue

    return width, _, hdr_format, commercial_name, channel_layout


def get_abbreviation(original_name, abbreviation_map=None):
    if abbreviation_map is None:
        abbreviation_map = load_abbreviation_map()
    return abbreviation_map.get(original_name, original_name)


def load_abbreviation_map(json_file_path="static/abbreviation.json"):
    try:
        with open(json_file_path, 'r') as file:
            abbreviation_map = json.load(file)
            logger.debug(f"加载缩写映射成功: {abbreviation_map}")
        return abbreviation_map
    except FileNotFoundError:
        logger.error(f"文件不存在: {json_file_path}")
        print(f"File not found: {json_file_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"解析文件失败: {json_file_path}")
        print(f"Error decoding JSON from file: {json_file_path}")
        return {}
