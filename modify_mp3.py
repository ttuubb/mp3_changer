import os
import datetime
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TPE1, TIT2
import logging

# --- 配置 ---
TARGET_DIR = "/home/ttuubb/下载"  # 更改为绝对路径
LOG_FILE = "modify_mp3.log"
# --- 配置结束 ---

# 设置日志记录
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(LOG_FILE, encoding='utf-8'),
                        logging.StreamHandler()
                    ])

def get_safe_filename(directory, base_name, extension):
    """生成一个安全、不重复的文件名"""
    counter = 1
    new_filename = f"{base_name}{extension}"
    full_path = os.path.join(directory, new_filename)
    while os.path.exists(full_path):
        new_filename = f"{base_name}_{counter}{extension}"
        full_path = os.path.join(directory, new_filename)
        counter += 1
    return new_filename

def process_mp3_file(filepath):
    """处理单个 MP3 文件"""
    try:
        audio = MP3(filepath, ID3=ID3)
        tags = audio.tags

        if tags is None:
            logging.warning(f"文件没有 ID3 标签，跳过元数据处理: {filepath}")
            tags = ID3() # 创建一个空的标签对象以便后续操作
            audio.tags = tags # 附加到 audio 对象

        # 1. 获取艺术家首字母
        artist = ""
        if 'TPE1' in tags:
            artist = str(tags['TPE1'].text[0]).strip()

        first_artist_char = 'X' # 默认值
        if artist:
            if len(artist) > 0:
                first_artist_char = artist[0]
            else:
                logging.warning(f"艺术家标签为空，将使用 'X' 代替: {os.path.basename(filepath)}")
        else:
            logging.warning(f"文件缺少艺术家标签，将使用 'X' 代替: {os.path.basename(filepath)}")

        if not os.path.exists(filepath):
            logging.error(f"文件不存在: {filepath}")
            return

        # 2. 获取日期并构造新基本文件名
        today_date = datetime.datetime.now().strftime("%Y%m%d")
        new_base_name = f"{today_date}{first_artist_char}"

        # 3. 清空艺术家和标题标签
        if 'TPE1' in tags:
            del tags['TPE1']
            logging.info(f"已清除艺术家标签: {os.path.basename(filepath)}")
        if 'TIT2' in tags:
            del tags['TIT2']
            logging.info(f"已清除标题标签: {os.path.basename(filepath)}")

        # 4. 移除封面图片 (APIC 帧)
        apic_frames = [key for key in tags.keys() if key.startswith('APIC')]
        if apic_frames:
            for frame_key in apic_frames:
                del tags[frame_key]
            logging.info(f"已移除 {len(apic_frames)} 个封面图片: {os.path.basename(filepath)}")
        else:
            logging.info(f"未找到封面图片: {os.path.basename(filepath)}")

        # 5. 保存元数据更改
        # Mutagen 在 MP3 对象上保存，而不是在 tags 对象上
        audio.save()
        logging.info(f"已保存元数据更改: {os.path.basename(filepath)}")

        # 6. 重命名文件
        directory = os.path.dirname(filepath)
        _, extension = os.path.splitext(filepath)
        new_filename = get_safe_filename(directory, new_base_name, extension)
        new_filepath = os.path.join(directory, new_filename)

        if filepath != new_filepath:
            os.rename(filepath, new_filepath)
            logging.info(f"文件已重命名: '{os.path.basename(filepath)}' -> '{new_filename}'")
        else:
             pass # 删除不必要的日志信息

    except Exception as e:
        logging.error(f"处理文件时出错 '{os.path.basename(filepath)}': {e}", exc_info=True)


def main():
    logging.info(f"开始处理目录: {TARGET_DIR}")
    if not os.path.isdir(TARGET_DIR):
        logging.error(f"错误：目标目录不存在或不是一个目录: {TARGET_DIR}")
        return

    processed_count = 0
    skipped_count = 0
    error_count = 0

    for filename in os.listdir(TARGET_DIR):
        if filename.lower().endswith(".mp3"):
            filepath = os.path.join(TARGET_DIR, filename)
            if os.path.isfile(filepath):
                logging.info(f"--- 开始处理: {filename} ---")
                try:
                    process_mp3_file(filepath)
                    processed_count += 1
                except Exception as e:
                    logging.error(f"处理文件时发生未捕获的异常 '{filename}': {e}", exc_info=True)
                    error_count += 1
                logging.info(f"--- 完成处理: {filename} ---")
            else:
                logging.warning(f"跳过，不是文件: {filename}")
                skipped_count += 1
        else:
            logging.debug(f"跳过，非 MP3 文件: {filename}") # 如果需要可以取消注释

    logging.info("="*30)
    logging.info(f"处理完成。")
    logging.info(f"成功处理: {processed_count} 个文件")
    logging.info(f"跳过: {skipped_count} 个项目")
    logging.info(f"出错: {error_count} 个文件")
    logging.info(f"详细日志请查看: {LOG_FILE}")
    logging.info("="*30)

if __name__ == "__main__":
    main()
