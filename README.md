# MP3 文件元数据修改工具

这是一个用于修改 MP3 文件元数据的 Python 工具。

## 功能

-   清除 MP3 文件的艺术家和标题标签。
-   移除 MP3 文件的封面图片。
-   根据艺术家首字母和当前日期重命名 MP3 文件。

## 使用方法

1.  安装依赖项：

    ```bash
    pip install -r requirements.txt
    ```

2.  运行脚本：

    ```bash
    python modify_mp3.py
    ```

## 依赖项

-   mutagen

## 配置

在 `modify_mp3.py` 文件中，可以配置以下选项：

-   `TARGET_DIR`:  要处理的 MP3 文件所在的目录。
-   `LOG_FILE`:  日志文件。
