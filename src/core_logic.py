"""
模块名称：core_logic.py
模块职责：负责核心业务逻辑处理
作者：D.C.Y.
创建时间：2025/03/14 15:35:12
最后修改时间：2025/03/21 23:59:20
"""

import random
from typing import Dict, Tuple


def generate_salary(job_type: str, company_name: str) -> str:
    """
    根据职位类型和公司名称智能生成薪资范围。

    :param job_type: 职位类型
    :param company_name: 公司全称
    :return: 薪资范围字符串，格式为"xk-yk"
    """
    # 解析公司所在地区和省份
    region, province = _parse_company_region(company_name)

    # 获取基准薪资范围
    base_range = _get_base_range(job_type, province)

    # 应用地区系数
    min_salary, max_salary = _apply_region_factor(base_range, region)

    # 应用公司规模系数
    if "巨头" in region:
        min_salary = int(min_salary * 1.2)
        max_salary = int(max_salary * 1.25)

    # 边界保护，确保薪资范围在合理区间内
    min_salary = max(15, min_salary)
    max_salary = min(100, max(max_salary, min_salary + 5))

    # 生成合理区间
    lower = random.randint(min_salary, max_salary - 5)
    upper = random.randint(lower + 5, max_salary)
    return f"{lower}k-{upper}k"


def _parse_company_region(company_name: str) -> Tuple[str, str]:
    """
    解析公司所属地区和省份。

    :param company_name: 公司全称
    :return: 地区和省份的元组
    """
    from data_definitions import REGION_CLASSIFICATION, BIGDATA_COMPANIES

    # 优先匹配互联网巨头
    for keyword in ["阿里", "腾讯", "百度", "字节", "华为", "京东", "美团", "拼多多"]:
        if keyword in company_name:
            return ("巨头", "巨头")

    # 匹配城市区域
    for city in REGION_CLASSIFICATION:
        if city in company_name:
            province = city if city in ["上海", "香港", "澳门"] else f"{city}省"
            return (REGION_CLASSIFICATION[city], province)

    return ("其他", "其他")


def _get_base_range(job_type: str, province: str) -> Tuple[int, int]:
    """
    获取基准薪资范围。

    :param job_type: 职位类型
    :param province: 省份
    :return: 基准薪资范围的元组
    """
    from data_definitions import PROVINCE_SALARY_RANGES

    # 职位类型系数
    job_coefficient = {
        "大数据开发": 1.0,
        "数据架构": 1.15,
        "数据分析": 0.9,
        "数据挖掘": 1.05,
        "数据科学家": 1.25
    }.get(job_type, 1.0)

    # 获取省份基准薪资范围
    base_min, base_max = PROVINCE_SALARY_RANGES.get(province, (18, 45))

    return (
        int(base_min * job_coefficient),
        int(base_max * job_coefficient)
    )


def _apply_region_factor(base_range: Tuple[int, int], region: str) -> Tuple[int, int]:
    """
    应用地区调节系数。

    :param base_range: 基准薪资范围
    :param region: 地区
    :return: 调节后的薪资范围
    """
    region_factor = {
        "长三角": 1.15,
        "珠三角": 1.10,
        "港澳": 1.30,
        "巨头": 1.25,
        "其他": 1.0
    }.get(region, 1.0)

    return (
        int(base_range[0] * region_factor),
        int(base_range[1] * region_factor)
    )


def generate_address() -> str:
    """
    增强版地址生成器，增加区域编号校验。

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
    生成合理的园区期数。

    :param template: 地址模板
    :return: 园区期数
    """
    if "厦门" in template:
        return random.choice([1, 2, 3])
    if "深圳" in template:
        return random.choice([1, 2])
    return random.randint(1, 5)
