"""
模块名称：core_logic.py
模块职责：核心逻辑处理模块
作者：D.C.Y.
创建时间：2025/03/14 15:35:12
最后修改时间：2025/03/21 23:59:20
"""
import random
from typing import Dict


def generate_salary(job_type: str) -> str:
    """
    动态薪资生成器（增强安全校验）
    :param job_type: 职位类型
    :return: 薪资范围字符串
    """
    salary_ranges: Dict[str, tuple] = {
        "大数据开发": (25, 50),
        "数据架构": (30, 60),
        "数据分析": (20, 40),
        "数据挖掘": (25, 45),
        "数据科学家": (35, 70)
    }

    # 安全获取范围
    min_salary, max_salary = salary_ranges.get(job_type, (20, 40))

    # 边界保护
    min_salary = max(15, min_salary)
    max_salary = min(100, max_salary)

    # 生成合理区间
    lower = random.randint(min_salary, max_salary - 5)
    upper = random.randint(lower + 5, max_salary)  # 确保区间有效性
    return f"{lower}k-{upper}k"


def generate_address() -> str:
    """
    增强版地址生成器（增加区域编号校验）
    :return: 生成的地址字符串
    """
    from data_definitions import ADDRESS_TEMPLATES

    try:
        template = random.choice(ADDRESS_TEMPLATES)
        if "软件园" in template:
            # 生成更合理的园区编号
            phase = _generate_phase_number(template)
            building = random.randint(101, 199) if "大厦" in template else random.randint(1, 50)
            return template.format(phase, building)
        elif "科技园" in template:
            return template.format(random.randint(1, 20))
        return template.format(random.randint(1, 99))
    except Exception as e:
        return "北京市海淀区中关村大街1号"


def _generate_phase_number(template: str) -> int:
    """
    生成合理的园区期数
    :param template: 地址模板
    :return: 园区期数
    """
    if "厦门" in template:
        return random.choice([1, 2, 3])
    if "深圳" in template:
        return random.choice([1, 2])
    return random.randint(1, 5)
