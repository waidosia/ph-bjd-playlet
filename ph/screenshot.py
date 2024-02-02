import json
import os
import random

import cv2
import numpy as np
import requests

from . import logger
from .tool import (generate_image_filename)
from requests.exceptions import RequestException


def create_directory(output_path):
    logger.info("创建输出路径")
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            logger.info("已创建输出路径")
            print("已创建输出路径")
    except PermissionError:
        logger.error("权限不足，无法创建目录")
        print("权限不足，无法创建目录。")
        return False, ["权限不足，无法创建目录。"]
    except FileExistsError:
        logger.error("路径已存在，且不是目录")
        print("路径已存在，且不是目录。")
        return False, ["路径已存在，且不是目录。"]
    except Exception as e:
        logger.error(f"创建目录时出错：{e}")
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
        logger.error("无法加载视频。")
        print("无法加载视频。")
        return False, ["无法加载视频。"]
    else:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps
        logger.info("加载视频成功")
        print("加载视频成功")

        # 计算起止时间帧编号
        start_frame = int(total_frames * start_pct)
        end_frame = int(total_frames * end_pct)
        min_interval = duration * min_interval_pct
        print("起止帧：" + str(start_frame) + " 终止帧：" + str(end_frame) + " 最小帧间隔" + str(min_interval))

        # 初始化变量
        extracted_images = []
        bbsurls = ""
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


def upload_screenshot(api_url, api_token, frame_path):
    logger.info("开始上传图床")
    print("开始上传图床")
    url = api_url

    # 判断frame_path为url还是本地路径
    if frame_path.startswith("http"):
        logger.info("输入一个在线图片链接")
        file_type = 'image/jpeg'
        # 请求文件拿到文件流
        try:
            res = requests.get(frame_path)
            logger.info("已成功获取文件流")
            print("已成功获取文件流")
        except RequestException as e:
            logger.error("请求过程中出现错误:" + str(e))
            print("请求过程中出现错误:", e)
            return False, {"请求过程中出现错误:" + str(e)}
        files = {'uploadedFile': (frame_path, res.content, file_type)}
    else:
        # Determine the MIME type based on file extension
        file_type = 'image/jpeg'  # default
        if frame_path.lower().endswith('.png'):
            file_type = 'image/png'
        elif frame_path.lower().endswith('.bmp'):
            file_type = 'image/bmp'
        elif frame_path.lower().endswith('.gif'):
            file_type = 'image/gif'
        elif frame_path.lower().endswith('.webp'):
            file_type = 'image/webp'

        files = {'uploadedFile': (frame_path, open(frame_path, 'rb'), file_type)}

    data = {'api_token': api_token, 'image_compress': 0, 'image_compress_level': 80}

    retry_count = 0
    while retry_count < 3:
        try:
            # 发送POST请求
            res = requests.post(url, data=data, files=files)
            logger.info("已成功发送上传图床的请求")
            print("已成功发送上传图床的请求")
            break  # 请求成功，跳出重试循环
        except RequestException as e:
            logger.error("请求过程中出现错误:" + str(e))
            print("请求过程中出现错误:", e)
            retry_count += 1
            if retry_count < 3:
                logger.info("进行第" + str(retry_count) + "次重试")
                print("进行第", retry_count, "次重试")
            else:
                logger.error("重试次数已用完")
                return False, {"请求过程中出现错误:" + str(e)}

    # 关闭文件流，避免资源泄露
    files['uploadedFile'][1].close()

    # 将响应文本转换为字典
    try:
        api_response = json.loads(res.text)
    except json.JSONDecodeError:
        logger.error("响应不是有效的JSON格式")
        print("响应不是有效的JSON格式")
        return False, {}

    # 返回完整的响应数据，以便进一步处理
    return True, api_response
