import datetime
import json
import os
import random
import re
import uuid
from tkinter import filedialog, Tk
from typing import Tuple

import cv2
import numpy as np
from pypinyin import pinyin, Style
from torf import Torrent


def update_settings(parameter_name, value) -> None:
    """
    将设置写入文件
    :param parameter_name: 设置字段的名称
    :param value: 设置字段的值
    :return: None
    """

    settings_file = os.path.join('static', 'settings.json')
    os.makedirs(os.path.dirname(settings_file), exist_ok=True)

    # 读取现有的设置
    settings = {}
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            settings = json.load(file)

    # 更新设置
    settings[parameter_name] = value

    # 写回文件
    with open(settings_file, 'w') as file:
        json.dump(settings, file, indent=4)


def get_settings(parameter_name) -> str or None:
    """
    从文件中获取设置
    :param parameter_name: 设置的字段名称
    :return: 设置字段的值
    """
    settings_file = os.path.join('static', 'settings.json')
    if not os.path.exists(settings_file):
        return None

    with open(settings_file, 'r') as file:
        settings = json.load(file)

    parameter_value = settings.get(parameter_name)
    print(f"{parameter_name}: {parameter_value}")
    return str(parameter_value)


def rename_file_with_same_extension(old_name, new_name_without_extension) -> tuple[bool, str]:
    """
    重命名文件，新文件名不包含扩展名
    :param old_name: 旧文件名
    :param new_name_without_extension: 新文件名（不包含扩展名）
    :return: 成功返回True和新文件名，失败返回False和错误信息
    """
    try:
        if not os.path.exists(old_name):
            print(f"未找到文件: '{old_name}'")
            return False, f"未找到文件: '{old_name}'"

        file_dir, file_base = os.path.split(old_name)
        file_name, file_extension = os.path.splitext(file_base)

        new_name = os.path.join(file_dir, new_name_without_extension + file_extension)

        os.rename(old_name, new_name)
        print(f"{old_name} 文件成功重命名为 {new_name}")
        return True, str(new_name)
    except OSError as e:
        print(f"重命名文件时出错: {e}")
        return False, f"重命名文件时出错: {e}"


def rename_directory(current_dir, new_name) -> Tuple[bool, str]:
    """
    重命名目录
    :param current_dir: 当前目录
    :param new_name: 新目录名
    :return: 成功返回True和新目录名，失败返回False和错误信息
    """
    try:
        if not os.path.exists(current_dir) or not os.path.isdir(current_dir):
            print("提供的路径不是一个目录或不存在。")
            raise ValueError("提供的路径不是一个目录或不存在。")

        parent_dir = os.path.dirname(current_dir)
        new_dir = os.path.join(parent_dir, new_name)

        os.rename(current_dir, new_dir)
        print(f"目录已重命名为: {new_dir}")
        return True, str(new_dir)
    except OSError as e:
        print(f"重命名目录时发生错误: {e}")
        return False, f"重命名目录时发生错误: {e}"


def generate_image_filename(base_path) -> str:
    """
    生成一个新的图片文件名
    :param base_path: 图片文件的基本路径
    :return: 新的图片文件名
    """
    now = datetime.datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    random_str = uuid.uuid4().hex[:6]
    filename = f"{date_time}_{random_str}.png"
    path = os.path.join(base_path, filename)
    return path


def get_file_path() -> str or None:
    """
    打开文件选择对话框，返回选择的文件路径
    :return: 选择的文件路径
    """
    file_types = [('Picture files', '*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.webp'),
                  ('All files', '*.*')]
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=file_types)
    return file_path


def get_folder_path() -> str or None:
    """
    打开文件夹选择对话框，返回选择的文件夹路径
    :return: 选择的文件夹路径
    """
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a folder")
    root.destroy()
    return folder_path


def check_path_and_find_video(path) -> tuple[int, str]:
    """
    检查路径是否是一个视频文件或文件夹，并返回视频文件路径
    :param path: 文件或文件夹路径
    :return: (1, 视频文件路径) 或 (2, 视频文件路径) 或 (0, 错误信息)
    """
    # 指定的视频文件类型列表
    VIDEO_EXTENSIONS = [".mp4", ".m4v", ".avi", ".flv", ".mkv", ".mpeg", ".mpg", ".rm", ".rmvb", ".ts", ".m2ts"]

    # 如果最后一位加了'/'则默认去除
    if path.endswith('/'):
        path = path[:-1]

    # 去除file:///
    if path.startswith('file:///'):
        path = path.replace('file:///', '', 1)

    # 检查路径是否是一个文件
    if os.path.isfile(path):
        _, ext = os.path.splitext(path)
        if ext.lower() in VIDEO_EXTENSIONS:
            return 1, path
        return 0, '是文件，但不符合视频类型'

    elif os.path.isdir(path):
        for entry in os.scandir(path):
            if entry.is_file():
                _, ext = os.path.splitext(entry.name)
                if ext.lower() in VIDEO_EXTENSIONS:
                    return 2, os.path.join(path, entry.name)
        return 0, '文件夹中没有符合类型的视频文件'
    else:
        return 0, '路径既不是文件也不是文件夹'


def get_video_files(folder_path) -> list:
    """
    获取文件夹中的视频文件列表
    :param folder_path: 文件夹路径
    :return: 视频文件列表
    """
    try:
        # 要查找的视频文件扩展名列表
        VIDEO_EXTENSIONS = [".mp4", ".m4v", ".avi", ".flv", ".mkv", ".mpeg", ".mpg", ".rm", ".rmvb", ".ts", ".m2ts"]
        # 检查文件夹路径是否有效和可访问
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            raise ValueError(f"提供的路径 '{folder_path}' 不是一个有效的目录。")
        # 初始化一个空列表来存储文件路径
        video_files = []
        # 遍历文件夹中的条目
        for entry in os.scandir(folder_path):
            if entry.is_file() and entry.name.lower().endswith(tuple(VIDEO_EXTENSIONS)):
                video_files.append(entry.path)
        # 对文件列表进行排序
        video_files.sort()
        return video_files

    except Exception as e:
        print(f"获取视频文件列表失败，错误原因: {e}")
        return []


def create_torrent(folder_path, torrent_path):
    """
    创建一个Torrent文件
    :param folder_path: 文件夹路径
    :param torrent_path: Torrent文件路径
    :return: 成功返回True和Torrent文件路径，失败返回False和错误信息
    """
    try:
        # 检查路径是否存在
        if not os.path.exists(folder_path):
            raise ValueError("Provided folder path does not exist.")

        # 检查路径是否指向一个非空目录或一个文件
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            raise ValueError("Provided folder path is empty.")

        # 构造完整的torrent文件路径
        torrent_file_name = os.path.basename(folder_path.rstrip("/\\")) + '.torrent'
        torrent_file_path = os.path.join(torrent_path, torrent_file_name)

        # 确保torrent文件的目录存在
        os.makedirs(os.path.dirname(torrent_file_path), exist_ok=True)

        # 如果目标 Torrent 文件已存在，则删除它
        if os.path.exists(torrent_file_path):
            os.remove(torrent_file_path)

        # 创建 Torrent 对象
        t = Torrent(path=folder_path, trackers=['https://tracker.example.com/announce'])

        # 生成和写入 Torrent 文件
        t.generate()
        t.write(torrent_file_path)

        print(f"Torrent created: {torrent_file_path}")
        return True, torrent_file_path

    except (OSError, IOError, ValueError) as e:
        # 捕获并处理文件操作相关的异常和值错误
        print(f"Error occurred: {e}")
        return False, str(e)

    except Exception as e:
        # 捕获所有其他异常
        print(f"An unexpected error occurred: {e}")
        return False, str(e)


def load_names(file_path, name):
    with open(file_path, 'r', encoding='utf-8') as file:  # 指定编码为utf-8
        data = json.load(file)
        return data[name]


def chinese_name_to_pinyin(chinese_name) -> str:
    """
    将中文名转换为拼音
    :param chinese_name: 中文名
    :return: 拼音
    """
    pinyin_list = pinyin(chinese_name, style=Style.NORMAL, heteronym=False)
    # 将拼音列表连接为字符串，且首字母大写
    pinyin_str = '.'.join([''.join(item) for item in pinyin_list]).title()
    return pinyin_str


# 从文件名中提取集数，
def get_episode_number(file_base) -> str or None:
    """
    从文件名中提取集数
    :param file_base: 文件名
    :return: 集数
    """
    match_e = re.search(r'E(\d+)', file_base)
    if match_e:
        return match_e.group(1)
    else:
        match_digits = re.search(r'(\d+)', file_base)
        if match_digits:
            return match_digits.group(1)
    return None


# 从文件名中提取集数，并返回重命名后的文件列表
def rename_video_files(video_files, file_name) -> list:
    """
    从文件名中提取集数，并返回重命名后的文件列表
    :param video_files: 视频文件列表
    :param file_name: 文件名
    :return: 重命名后的文件列表
    """
    renamed_files = []
    for video_file in video_files:
        _, file_base = os.path.split(video_file)
        episode_number = get_episode_number(file_base)
        if episode_number is None:
            print("提取集数失败，退出")
            break
        episode_number = str(episode_number).zfill(len(str(len(video_files))))
        is_success, renamed_file = rename_file_with_same_extension(video_file, file_name.replace('??', episode_number))
        if is_success:
            renamed_files.append(renamed_file)
    return renamed_files


def rename_directory_if_needed(video_path, file_name) -> str | None:
    """
    如果文件夹名中包含E??，则重命名文件夹
    :param video_path: 视频文件路径
    :param file_name: 文件名
    :return: None
    """
    directory_path = os.path.dirname(video_path)
    if 'E??' in file_name:
        is_success, rename_dir = rename_directory(directory_path, file_name.replace('E??', ''))
        if is_success:
            return rename_dir
        return None
    return None


def extract_and_get_thumbnails(videoPath, screenshotPath, screenshotNumber, screenshotThreshold,
                               screenshotStart, screenshotEnd, getThumbnails, rows, cols):
    images = {}

    # 执行截图函数
    screenshot_success, res = extract_complex_keyframes(videoPath, screenshotPath, screenshotNumber,
                                                        screenshotThreshold, screenshotStart,
                                                        screenshotEnd, min_interval_pct=0.01)
    images['screenshot'] = res

    # 获取缩略图
    if getThumbnails:
        get_thumbnails_success, sv_path = get_thumbnails(videoPath, screenshotPath, rows, cols, screenshotStart,
                                                         screenshotEnd)
        if get_thumbnails_success:
            # res.append(sv_path)
            images['thumbnails'] = sv_path

    return screenshot_success, images


def create_directory(output_path):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

            print("已创建输出路径")
    except PermissionError:
        print("权限不足，无法创建目录。")
        return False, ["权限不足，无法创建目录。"]
    except FileExistsError:
        print("路径已存在，且不是目录。")
        return False, ["路径已存在，且不是目录。"]
    except Exception as e:
        print(f"创建目录时出错：{e}")
        return False, [f"创建目录时出错：{e}"]
    return True, []


def extract_complex_keyframes(video_path, output_path, num_images, some_threshold, start_pct, end_pct,
                              min_interval_pct=0.01):
    success, error_message = create_directory(output_path)
    if not success:
        return False, error_message

    # 加载视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无法加载视频。")
        return False, ["无法加载视频。"]
    else:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps
        print("加载视频成功")

        # 计算起止时间帧编号
        start_frame = int(total_frames * start_pct)
        end_frame = int(total_frames * end_pct)
        min_interval = duration * min_interval_pct
        print("起止帧：" + str(start_frame) + " 终止帧：" + str(end_frame) + " 最小帧间隔" + str(min_interval))

        # 初始化变量
        extracted_images = []
        last_keyframe_time = -min_interval

        # 生成随机时间戳
        timestamps = sorted(random.sample(range(start_frame, end_frame), num_images))

        for timestamp in timestamps:
            # 跳转到特定帧
            cap.set(cv2.CAP_PROP_POS_FRAMES, timestamp)
            ret, frame = cap.read()
            if not ret:
                continue

            current_time = timestamp / fps
            if current_time >= last_keyframe_time + min_interval:
                std_dev = np.std(frame)
                print(f"Frame ID: {timestamp}, Timestamp: {current_time}, Std Dev: {std_dev}")  # 调试信息

                if std_dev > some_threshold:
                    frame_path = generate_image_filename(output_path)
                    cv2.imwrite(frame_path, frame)
                    extracted_images.append(frame_path)
                    last_keyframe_time = current_time

        cap.release()

        print(extracted_images)
        return True, extracted_images


def get_thumbnails(video_path, output_path, cols, rows, start_pct, end_pct):
    global video_capture
    success, error_message = create_directory(output_path)
    if not success:
        return False, error_message

    try:
        video_capture = cv2.VideoCapture(video_path)

        if not video_capture.isOpened():
            raise Exception("Error: 无法打开视频文件")

        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        # 计算开始和结束帧
        start_frame = int(total_frames * start_pct)
        end_frame = int(total_frames * end_pct)

        # 计算每张截取图像的时间间隔
        interval = (end_frame - start_frame) // (rows * cols)

        images = []

        for i, _ in enumerate(range(rows * cols)):
            frame_number = start_frame + i * interval
            if frame_number >= end_frame:
                break

            video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = video_capture.read()

            if not ret:
                raise Exception(f"Error: 无法读取第 {i + 1} 张图像")

            images.append(frame)

        # 处理图像数量小于预期的情况
        if len(images) < (rows * cols):
            print(f"Warning: 只能获取 {len(images)} 张图像，小于预期的 {rows * cols} 张")

        resized_images = [cv2.resize(image, (0, 0), fx=1.0 / cols, fy=1.0 / cols) for image in images]

        border_size = 5
        concatenated_image = np.ones((rows * (resized_images[0].shape[0] + 2 * border_size),
                                      cols * (resized_images[0].shape[1] + 2 * border_size), 3), dtype=np.uint8) * 255

        for i, image in enumerate(resized_images):
            y_offset = i // cols * (image.shape[0] + 2 * border_size) + border_size
            x_offset = i % cols * (image.shape[1] + 2 * border_size) + border_size
            concatenated_image[y_offset:y_offset + image.shape[0],
            x_offset:x_offset + image.shape[1]] = image

        sv_path = generate_image_filename(output_path)
        cv2.imwrite(sv_path, concatenated_image)

    except Exception as e:
        print(f"发生异常: {e}")
        return False, str(e)

    finally:
        video_capture.release()

    print(f"拼接后的图像已保存到{sv_path}")
    return True, sv_path


def replace_fullwidth_symbols(text):
    replacements = {
        '，': ',',  # 中文逗号替换为英文逗号
        '。': '.',  # 中文句号替换为英文句号
        '！': '!',  # 中文感叹号替换为英文感叹号
        '？': '?',  # 中文问号替换为英文问号
        '；': ';',  # 中文分号替换为英文分号
        '：': ':',  # 中文冒号替换为英文冒号
        '“': '"',  # 中文左双引号替换为英文双引号
        '”': '"',  # 中文右双引号替换为英文双引号
        '‘': "'",  # 中文左单引号替换为英文单引号
        '’': "'",  # 中文右单引号替换为英文单引号
        # 添加其他需要替换的符号对
    }
    result = ""
    for char in text:
        if char in replacements:
            char = replacements[char]
        result += char
    return result
