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
    # 修改为 http:// 格式的地址
    hdfs_client = InsecureClient('http://master:9870', user='root')
    _clear_hdfs_directories(hdfs_client)
    _create_hdfs_directories(hdfs_client)

    total_files = 30
    for file_index in range(1, total_files + 1):
        global dataset
        dataset = _generate_batch(1000)
        _print_progress(file_index, total_files)
        _upload_to_hdfs(file_index, hdfs_client, dataset)

    print("数据已成功上传到 HDFS...")


def _clear_hdfs_directories(hdfs_client):
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


def _create_hdfs_directories(hdfs_client):
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


def _generate_batch(batch_size: int) -> List[dict]:
    """
    生成批量数据
    :param batch_size: 批量数据的数量
    :return: 包含多个职位信息的列表
    """
    return [generate_job_record() for _ in range(batch_size)]


def _print_progress(current: int, total: int):
    """
    带颜色的进度显示
    :param current: 当前进度
    :param total: 总进度
    """
    progress = current / total * 100
    bar = f"[{'#' * int(progress // 3.33)}{' ' * (30 - int(progress // 3.33))}]"
    print(f"\r生成进度: {bar} {progress:.1f}%", end="")
    if current == total:
        print(f"\n模拟数据生成完毕...\n"
              f"共生成{total}个文件，每个文件有{len(dataset)}个职位信息...\n"
              f"请检查 HDFS 目录 /JobData 和 /JobData-Json")


def _upload_to_hdfs(file_index: int, hdfs_client, dataset):
    """
    将生成的数据文件上传到 HDFS
    :param file_index: 文件索引
    :param hdfs_client: HDFS 客户端
    :param dataset: 数据集
    """
    validated_data = []
    for record in dataset:
        # 强制字段校验
        if not all(record.get(field) for field in ["positionId", "companyFullName", "positionName"]):
            continue

        # 自动修复薪资格式
        if "-" not in record["salary"]:
            record["salary"] = "20k-30k"
        validated_data.append(record)

    # 保存无扩展名版本
    hdfs_path_no_ext = f"/JobData/{datetime.now().strftime('%Y%m%d')}/page{file_index}"
    try:
        with hdfs_client.write(hdfs_path_no_ext, encoding='utf-8') as writer:
            json.dump(dataset, writer, ensure_ascii=False, indent=2)
        print(f"\t已成功上传 {hdfs_path_no_ext} 到 HDFS...")
    except Exception as e:
        print(f"\t上传 {hdfs_path_no_ext} 到 HDFS 失败: {str(e)}")
        print("请检查 HDFS 服务配置和网络连接...")


if __name__ == "__main__":
    main()
