import json
import os

from pymediainfo import MediaInfo

from util.log import logger


def get_media_info(file_path):
    logger.info("开始获取视频信息")
    if not os.path.exists(file_path):
        logger.error("文件路径不存在")
        print("文件路径不存在")
        return False, "视频文件路径不存在"
    original_working_directory = os.getcwd()
    # 获取上一级目录的路径
    parent_directory = os.path.abspath(os.path.join(file_path, os.pardir))
    # 将文件路径转换为相对于当前工作目录的相对路径
    relative_file_path = os.path.relpath(file_path, parent_directory)
    # 切换到上一级目录
    os.chdir(parent_directory)
    logger.info(f"切换到新的工作目录 {parent_directory}")
    try:
        # 尝试解析媒体信息
        media_info = MediaInfo.parse(relative_file_path)
        json_data = media_info.to_json()
        # 解析 JSON 数据
        data = json.loads(json_data)
        # 初始化输出字符串
        output = ""
        # 遍历所有 track
        for track in data["tracks"]:
            track_type = track["track_type"]
            if track_type == "General":
                output += handle_general_track(track)
            elif track_type == "Video":
                output += handle_video_track(track)
            elif track_type == "Audio":
                output += handle_audio_track(track)
            elif track_type == "Text":
                output += handle_text_track(track)

        return True, output
    except OSError as e:
        # 文件路径相关的错误
        logger.error(f"文件路径错误: {e}")
        print(f"文件路径错误: {e}")
        return False, f"文件路径错误: {e}"
    except Exception as e:
        logger.error(f"无法解析文件: {e}")
        # MediaInfo无法解析文件
        print(f"无法解析文件: {e}")
        return False, f"无法解析文件: {e}"
    finally:
        # 恢复工作目录
        logger.info("恢复工作目录")
        os.chdir(original_working_directory)


def handle_general_track(track):
    output = "General\n"
    for key, label in [
        ("other_unique_id", "Unique ID"),
        ("complete_name", "Complete name"),
        ("other_format", "Format"),
        ("format_version", "Format version"),
        ("other_file_size", "File size"),
        ("other_duration", "Duration"),
        ("other_overall_bit_rate_mode", "Overall bit rate mode"),
        ("other_overall_bit_rate", "Overall bit rate"),
        ("other_frame_rate", "Frame rate"),
        ("movie_name", "Movie name"),
        ("encoded_date", "Encoded date"),
        ("writing_application", "Writing application"),
        ("writing_library", "Writing library"),
        ("comment", "Comment")
    ]:

        value = track[key][0] if isinstance(track.get(key), list) else track.get(key)
        if value is not None:
            output += f"{label:36}: {value}\n"
    output += "\n"
    return output


def handle_video_track(track):
    output = "Video\n"
    for key, label in [
        ("track_id", "ID"),
        ("other_format", "Format"),
        ("format_info", "Format/Info"),
        ("format_settings", "Format settings"),
        ("format_settings__cabac", "Format settings, CABAC"),
        ("other_format_settings__reference_frames", "Format settings, Reference frames"),
        ("other_hdr_format", "HDR format"),
        ("codec_id", "Codec ID"),
        ("other_duration", "Duration"),
        ("other_bit_rate", "Bit rate"),
        ("other_width", "Width"),
        ("other_height", "Height"),
        ("other_display_aspect_ratio", "Display aspect ratio"),
        ("other_frame_rate_mode", "Frame rate mode"),
        ("other_frame_rate", "Frame rate"),
        ("color_space", "Color space"),
        ("other_chroma_subsampling", "Chroma subsampling"),
        ("other_bit_depth", "Bit depth"),
        ("scan_type", "Scan type"),
        ("bits__pixel_frame", "Bits/(Pixel*Frame)"),
        ("other_stream_size", "Stream size"),
        ("other_writing_library", "Writing library"),
        ("encoding_settings", "Encoding settings"),
        ("default", "Default"),
        ("forced", "Forced"),
        ("color_range", "Color range"),
        ("color_primaries", "Color primaries"),
        ("transfer_characteristics", "Transfer characteristics"),
        ("matrix_coefficients", "Matrix coefficients"),
        ("mastering_display_color_primaries", "Mastering display color primaries"),
        ("mastering_display_luminance", "Mastering display luminance"),
        ("maximum_content_light_level", "Maximum Content Light Level"),
        ("maxcll_original", "MaxCLL Original"),
        ("maximum_frameaverage_light_level", "Maximum Frame-Average Light Level"),
        ("maxfall_original", "MaxFALL Original"),
    ]:
        value = track[key][0] if isinstance(track.get(key), list) else track.get(key)
        if value is not None:
            output += f"{label:36}: {value}\n"
    output += "\n"
    return output


def handle_audio_track(track):
    output = f"\nAudio #{track['track_id']}\n"
    for key, label in [
        ("track_id", "ID"),
        ("other_format", "Format"),
        ("format_info", "Format/Info"),
        ("other_commercial_name", "Commercial name"),
        ("codec_id", "Codec ID"),
        ("other_duration", "Duration"),
        ("other_bit_rate_mode", "Bit rate mode"),
        ("other_bit_rate", "Bit rate"),
        ("other_maximum_bit_rate", "Maximum bit rate"),
        ("other_channel_s", "Channel(s)"),
        ("channel_layout", "Channel layout"),
        ("other_sampling_rate", "Sampling rate"),
        ("other_frame_rate", "Frame rate"),
        ("other_compression_mode", "Compression mode"),
        ("other_delay_relative_to_video", "Delay relative to video"),
        ("other_stream_size", "Stream size"),
        ("title", "Title"),
        ("other_language", "Language"),
        ("default", "Default"),
        ("forced", "Forced"),
        ("complexity_index", "Complexity index"),
        ("number_of_dynamic_objects", "Number of dynamic objects"),
        ("other_bed_channel_count", "Bed channel count"),
        ("bed_channel_configuration", "Bed channel configuration"),
    ]:
        value = track[key][0] if isinstance(track.get(key), list) else track.get(key)
        if value is not None:
            output += f"{label:36}: {value}\n"
    output += "\n"
    return output


def handle_text_track(track):
    output = f"\nText #{track['other_track_id']}\n"
    for key, label in [
        ("other_track_id", "ID"),
        ("other_format", "Format"),
        ("muxing_mode", "Muxing mode"),
        ("codec_id", "Codec ID"),
        ("codec_id_info", "Codec ID/Info"),
        ("other_duration", "Duration"),
        ("other_bit_rate", "Bit rate"),
        ("other_frame_rate", "Frame rate"),
        ("count_of_elements", "Count of elements"),
        ("other_stream_size", "Stream size"),
        ("title", "Title"),
        ("other_language", "Language"),
        ("default", "Default"),
        ("forced", "Forced"),
    ]:
        value = track[key][0] if isinstance(track.get(key), list) else track.get(key)
        if value is not None:
            output += f"{label:36}: {value}\n"
    output += "\n"
    return output
