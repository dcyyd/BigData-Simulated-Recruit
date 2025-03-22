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
    _create_directories()

    total_files = 30
    for file_index in range(1, total_files + 1):
        global dataset
        dataset = _generate_batch(1000)
        _save_data(file_index, dataset)
        _print_progress(file_index, total_files)


def _create_directories():
    """
    安全创建存储目录
    """
    dirs = ["../JobData", "../JobData-Json"]
    for d in dirs:
        try:
            os.makedirs(d, exist_ok=True)
            # 设置目录权限（仅限当前用户）
            os.chmod(d, 0o700)
        except OSError as e:
            raise SystemExit(f"目录创建失败: {e.strerror}")


def _generate_batch(batch_size: int) -> List[dict]:
    """
    生成批量数据
    :param batch_size: 批量数据的数量
    :return: 包含多个职位信息的列表
    """
    return [generate_job_record() for _ in range(batch_size)]


def _save_data(file_index: int, dataset: List[dict]):
    """
    保存数据前进行完整性校验
    :param file_index: 文件索引
    :param dataset: 包含多个职位信息的列表
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

    try:
        # 保存无扩展名版本
        with open(f"../JobData/page{file_index}", "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)

        # 保存JSON版本
        with open(f"../JobData-Json/page{file_index}.json", "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)

    except IOError as e:
        print(f"文件保存失败: {str(e)}")


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
              f"请检查目录../JobData和../JobData-Json")


if __name__ == "__main__":
    main()
