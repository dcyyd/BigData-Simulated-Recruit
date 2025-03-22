"""
模块名称：data_generation.py
模块职责：生成职位数据
作者：D.C.Y.
创建时间：2025/03/14 15:34:51
最后修改时间：2025/03/22 0:10:11
"""
from copy import deepcopy
import random
from faker import Faker
from typing import Dict, List

# 导入依赖模块
from data_definitions import (
    BIGDATA_COMPANIES,
    INDUSTRY_FIELDS,
    TECH_REQUIREMENTS,
    APPLICATION_REQUIREMENTS,
    POSITION_REQUIREMENTS,
    WELFARE_OPTIONS,
    POSITION_ADVANTAGES,
    EXTRA_TAGS,
    GENERAL_TAGS,
    BASE_TEMPLATE
)
from core_logic import generate_salary, generate_address

fake = Faker("zh_CN")
_generated_ids = set()


def generate_job_record() -> Dict:
    """
    生成单个职位记录（带完整性校验）
    :return: 包含职位信息的字典
    """
    job_type = _get_valid_job_type()
    record = _build_base_record(job_type)
    _add_dynamic_fields(record, job_type)
    _ensure_data_integrity(record)
    return record


def _get_valid_job_type() -> str:
    """
    获取有效职位类型
    :return: 随机选择的有效职位类型
    """
    return random.choice(list(TECH_REQUIREMENTS.keys()))


def _build_base_record(job_type: str) -> Dict:
    """
    构建完整的基础记录结构
    :param job_type: 职位类型
    :return: 包含基础职位信息的字典
    """
    record = deepcopy(BASE_TEMPLATE)
    company_name = random.choice(BIGDATA_COMPANIES)

    record.update({
        "companyFullName": company_name,
        "companyShortName": _generate_short_name(company_name),
        "companyType": random.choice(["上市公司", "独角兽", "行业龙头", "创业公司"]),
        "financeStage": random.choice(["已上市", "D轮及以上", "C轮", "B轮", "A轮", "天使轮"]),
        "companySize": random.choice(["100-499人", "500-999人", "1000-9999人", "10000人以上"]),
        "industryField": random.choice(INDUSTRY_FIELDS),
        "businessArea": random.sample(INDUSTRY_FIELDS, k=random.randint(1, 3)) if random.random() > 0.1 else None,
        "workAddress": generate_address(),
        "positionName": f"{job_type}工程师",
        "firstType": job_type,
        "education": random.choice(["本科", "硕士", "博士"]) if random.random() > 0.05 else None,  # 5%缺失率
        "workYear": f"{random.randint(1, 3)}-{random.randint(4, 8)}年" if random.random() > 0.05 else None,
        "salary": generate_salary(job_type),
        "jobDescription": f"负责{job_type}相关工作，包括：{_generate_job_description(job_type)}",
        "positionId": _generate_unique_id(),
        "formatCreateTime": fake.date_between(start_date="-1y").isoformat()
    })
    return record


def _add_dynamic_fields(record: Dict, job_type: str):
    """
    添加完整动态字段
    :param record: 包含基础职位信息的字典
    :param job_type: 职位类型
    """
    # 福利（80%生成概率）
    if random.random() > 0.2:
        record["welfare"] = random.sample(WELFARE_OPTIONS, k=random.randint(2, 5))

    # 岗位优势（70%生成概率）
    if random.random() > 0.3:
        record["positionAdvantage"] = random.choice(POSITION_ADVANTAGES)

    # 技术要求（90%生成概率）
    if random.random() > 0.1:
        record["requirements"] = POSITION_REQUIREMENTS[job_type]

    # 申请要求（80%生成概率）
    if random.random() > 0.2:
        record["applicationRequirements"] = random.sample(
            APPLICATION_REQUIREMENTS[job_type],
            k=random.randint(2, 3)
        )

    # 技术标签（95%生成概率）
    if random.random() > 0.05:
        tech_tags = (
                TECH_REQUIREMENTS[job_type][:3] +
                ["大数据平台" if "数据" in job_type else "业务分析"] +
                [f"{job_type}认证优先"] +
                random.sample(EXTRA_TAGS.get(job_type, []), 3) +
                random.sample(GENERAL_TAGS, 2)
        )
        record["positionLables"] = tech_tags


def _generate_short_name(company_name: str) -> str:
    """
    生成公司简称
    :param company_name: 公司全称
    :return: 公司简称
    """
    name_map = {
        "阿里云数据科技": "阿里云",
        "腾讯大数据中心": "腾讯云",
        "华为数据工程部": "华为云",
        "京东数科": "京东云",
        "IBM中国大数据实验室": "IBM实验室"
    }
    return name_map.get(company_name, company_name[:4] + "数据")


def _generate_job_description(job_type: str) -> str:
    """
    生成个性化职位描述
    :param job_type: 职位类型
    :return: 职位描述字符串
    """
    descriptions = {
        "大数据开发": ["数据平台搭建", "ETL流程优化", "实时计算系统维护"],
        "数据分析": ["业务指标分析", "数据可视化呈现", "AB测试设计"],
        "数据挖掘": ["用户行为建模", "推荐算法优化", "数据特征工程"],
        "数据架构": ["数据模型设计", "元数据管理", "数据治理体系搭建"],
        "数据科学家": ["机器学习模型开发", "数据驱动决策支持", "因果推理分析"]
    }
    return "、".join(random.sample(descriptions[job_type], 3))


def _generate_unique_id() -> int:
    """
    生成唯一ID（防止冲突）
    :return: 唯一的ID
    """
    while True:
        new_id = random.randint(10 ** 6, 10 ** 7)
        if new_id not in _generated_ids:
            _generated_ids.add(new_id)
            return new_id


def _ensure_data_integrity(record: Dict):
    """
    数据完整性校验
    :param record: 包含职位信息的字典
    """
    # 强制字段校验
    mandatory_fields = ["positionId", "companyFullName", "positionName"]
    for field in mandatory_fields:
        if not record.get(field):
            raise ValueError(f"关键字段缺失: {field}")

    # 薪资格式校验
    if "-" not in record["salary"]:
        record["salary"] = "20k-30k"
