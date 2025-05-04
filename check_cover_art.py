import sys
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import logging

# 配置日志（可选，但有助于调试）
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def check_apic_frames(filepath):
    """检查 MP3 文件是否包含 APIC (封面图片) 帧"""
    try:
        audio = MP3(filepath, ID3=ID3)
        if audio.tags is None:
            logging.info(f"文件 '{filepath}' 没有 ID3 标签。")
            return False # 没有标签，自然没有图片

        apic_frames = [key for key in audio.tags.keys() if key.startswith('APIC')]

        if apic_frames:
            logging.warning(f"在文件 '{filepath}' 中找到 {len(apic_frames)} 个 APIC 帧 (封面图片)。")
            # 可以选择性地打印帧信息
            # for frame_key in apic_frames:
            #     frame = audio.tags[frame_key]
            #     logging.debug(f"  - Frame: {frame_key}, MimeType: {frame.mime}, Desc: {frame.desc}")
            return True
        else:
            logging.info(f"在文件 '{filepath}' 中未找到 APIC 帧 (封面图片)。")
            return False

    except Exception as e:
        logging.error(f"检查文件 '{filepath}' 时出错: {e}", exc_info=True)
        return None # 表示检查出错

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python check_cover_art.py <mp3_file_path>")
        sys.exit(1)

    mp3_file = sys.argv[1]
    result = check_apic_frames(mp3_file)

    if result is True:
        print(f"结果：文件 '{mp3_file}' 仍然包含封面图片。")
        sys.exit(1) # 返回非零表示找到图片
    elif result is False:
        print(f"结果：文件 '{mp3_file}' 不包含封面图片。")
        sys.exit(0) # 返回零表示未找到图片
    else:
        print(f"结果：检查文件 '{mp3_file}' 时发生错误。")
        sys.exit(2) # 返回其他值表示错误
