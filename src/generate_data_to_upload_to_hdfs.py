import json
from datetime import datetime
from typing import List
from data_generation import generate_job_record
from hdfs import InsecureClient

"""
模块名称：generate_data_to_upload_to_hdfs.py
模块职责：该脚本用于生成模拟的职位信息数据，并将其上传到 HDFS。
作者: D.C.Y.
创建日期: 2025/03/14 15:32:12
最后修改日期: 2025/03/22 1:34:45
"""


def main():
    """
    主执行函数
    """
    hdfs_client = InsecureClient('http://master:9870', user='root')
    initialize_hdfs_directories(hdfs_client)

    total_files = 30
    batch_size = 1000  # 定义 batch_size 变量
    for file_index in range(1, total_files + 1):
        dataset = generate_batch_data(batch_size)
        print_progress(file_index, total_files, batch_size)  # 传递 batch_size 参数
        upload_data_to_hdfs(file_index, hdfs_client, dataset)

    print("数据已成功上传到 HDFS...")


def initialize_hdfs_directories(hdfs_client):
    """
    初始化 HDFS 目录，包括清空和创建目录
    """
    clear_hdfs_directories(hdfs_client)
    create_hdfs_directories(hdfs_client)


def clear_hdfs_directories(hdfs_client):
    """
    清空 HDFS 根目录和指定文件夹
    """
    directories = ["/JobData"]
    for directory in directories:
        try:
            if hdfs_client.status(directory, strict=False):
                hdfs_client.delete(directory, recursive=True)
                print(f"已清空 HDFS 目录: {directory}")
        except Exception as e:
            print(f"清空 HDFS 目录 {directory} 失败: {str(e)}")


def create_hdfs_directories(hdfs_client):
    """
    在 HDFS 上创建存储目录
    """
    dirs = ["/JobData"]
    for d in dirs:
        try:
            hdfs_client.makedirs(d)
            print(f"已在 HDFS 上创建目录: {d}")
        except Exception as e:
            print(f"在 HDFS 上创建目录 {d} 失败: {str(e)}")


def generate_batch_data(batch_size: int) -> List[dict]:
    """
    生成批量数据
    :param batch_size: 批量数据的数量
    :return: 包含多个职位信息的列表
    """
    return [generate_job_record() for _ in range(batch_size)]


def print_progress(current: int, total: int, batch_size: int):
    """
    带颜色的进度显示
    :param current: 当前进度
    :param total: 总进度
    :param batch_size: 每个文件包含的职位信息数量
    """
    progress = current / total * 100
    bar = f"[{'#' * int(progress // 3.33)}{' ' * (30 - int(progress // 3.33))}]"
    print(f"\r生成进度: {bar} {progress:.1f}%", end="")
    if current == total:
        print(f"\n模拟数据生成完毕...\n"
              f"共生成{total}个文件，每个文件有{batch_size}个职位信息...\n"
              f"请检查 HDFS 目录 /JobData")


def upload_data_to_hdfs(file_index: int, hdfs_client, dataset):
    """
    将生成的数据文件上传到 HDFS
    :param file_index: 文件索引
    :param hdfs_client: HDFS 客户端
    :param dataset: 数据集
    """
    validated_data = validate_and_fix_data(dataset)

    # 保存为JSON Lines格式
    hdfs_path = f"/JobData/{datetime.now().strftime('%Y%m%d')}/page{file_index}.json"
    try:
        with hdfs_client.write(hdfs_path, encoding='utf-8') as writer:
            for record in validated_data:
                json_line = json.dumps(record, ensure_ascii=False, separators=(',', ':'))
                writer.write(json_line + ',')  # 添加逗号分隔符
    except Exception as e:
        print(f"\t上传 {hdfs_path} 到 HDFS 失败: {str(e)}")


def validate_and_fix_data(dataset: List[dict]) -> List[dict]:
    """
    验证并修复数据
    :param dataset: 原始数据集
    :return: 验证和修复后的数据集
    """
    validated_data = []
    for record in dataset:
        # 强制字段校验
        if not all(record.get(field) for field in ["positionId", "companyFullName", "positionName"]):
            continue

        # 自动修复薪资格式
        if "-" not in record["salary"]:
            record["salary"] = "10k-25k"  # 默认值
        validated_data.append(record)

    return validated_data


if __name__ == "__main__":
    main()
