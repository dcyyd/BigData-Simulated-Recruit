"""
模块名称：generate_data_to_windows.py
模块功能：生成职位数据并保存到Windows系统
作者：D.C.Y.
创建时间：2025/03/14 15:32:12
最后修改时间：2025/03/22 0:34:45
"""
import os
import json
from typing import List
from data_generation import generate_job_record


def main():
    """
    主执行函数
    """
    initialize_directories()

    total_files = 30
    for file_index in range(1, total_files + 1):
        dataset = generate_batch_data(1000)
        save_data(file_index, dataset)
        print_progress(file_index, total_files, dataset)  # 传递 dataset 参数


def initialize_directories():
    """
    安全创建存储目录
    """
    dirs = ["../JobData", "../JobData-Json"]
    for d in dirs:
        try:
            os.makedirs(d, exist_ok=True)
            os.chmod(d, 0o700)  # 设置目录权限（仅限当前用户）
        except OSError as e:
            raise SystemExit(f"目录创建失败: {e.strerror}")


def generate_batch_data(batch_size: int) -> List[dict]:
    """
    生成批量数据
    :param batch_size: 批量数据的数量
    :return: 包含多个职位信息的列表
    """
    return [generate_job_record() for _ in range(batch_size)]


def save_data(file_index: int, dataset: List[dict]):
    """
    保存数据前进行完整性校验
    :param file_index: 文件索引
    :param dataset: 包含多个职位信息的列表
    """
    validated_data = validate_and_fix_data(dataset)

    try:
        # 保存无扩展名版本
        with open(f"../JobData/page{file_index}", "w", encoding="utf-8") as f:
            for record in validated_data:
                json_line = json.dumps(record, ensure_ascii=False, separators=(',', ':'))  # 使用紧凑格式
                f.write(json_line + ',')  # 每个记录用逗号分隔

        # 保存为JSON Lines格式（.json）
        with open(f"../JobData-Json/page{file_index}.json", "w", encoding="utf-8") as f:
            for record in validated_data:
                json_line = json.dumps(record, ensure_ascii=False, separators=(',', ':'))  # 使用紧凑格式
                f.write(json_line + ',')  # 每个记录用逗号分隔

    except IOError as e:
        print(f"文件保存失败: {str(e)}")


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
            record["salary"] = "15k-25k"

        validated_data.append(record)

    return validated_data


def print_progress(current: int, total: int, dataset):
    """
    带颜色的进度显示
    :param current: 当前进度
    :param total: 总进度
    :param dataset: 数据集
    """
    progress = current / total * 100
    bar = f"[{'#' * int(progress // 3.33)}{' ' * (30 - int(progress // 3.33))}]"
    print(f"\r生成进度: {bar} {progress:.1f}%", end="")
    if current == total:
        print(f"\n模拟数据生成完毕...\n"
              f"共生成{total}个文件，每个文件有{len(dataset)}个招聘信息...\n"
              f"请检查目录../JobData和../JobData-Json")


if __name__ == "__main__":
    main()
