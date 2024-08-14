import logging


import logging
import os
import sys


def setup_logger(name=None, log_file=None, level=logging.INFO):
    """
    设置日志配置
    :param name: logger名称，如果为None，则配置根logger
    :param log_file: 日志文件路径。如果为None，则根据脚本名称自动生成
    :param level: 日志级别
    :return: 配置好的logger
    """
    logger = logging.getLogger(name)

    # 检查是否已经有handler，避免重复添加
    if not logger.hasHandlers():
        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )

        # 自动生成日志文件名
        if log_file is None:
            script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
            log_file = f"{script_name}.log"

        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 文件处理器
        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
