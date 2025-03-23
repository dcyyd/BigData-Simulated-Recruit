"""
模块名称：data_generation.py
模块职责：生成职位数据
作者：D.C.Y.
创建时间：2025/03/14 15:34:51
最后修改时间：2025/03/22 0:10:11
"""
from copy import deepcopy  # 导入deepcopy函数，用于深拷贝字典
import random  # 导入random模块，用于生成随机数据
from faker import Faker  # 导入Faker模块，用于生成假数据
from typing import Dict, List  # 导入Dict和List类型提示

# 导入依赖模块
from data_definitions import (
    BIGDATA_COMPANIES,  # 大数据公司列表
    INDUSTRY_FIELDS,  # 行业领域列表
    TECH_REQUIREMENTS,  # 技术要求字典
    APPLICATION_REQUIREMENTS,  # 申请要求字典
    POSITION_REQUIREMENTS,  # 职位要求字典
    WELFARE_OPTIONS,  # 福利选项列表
    POSITION_ADVANTAGES,  # 职位优势列表
    EXTRA_TAGS,  # 额外标签字典
    GENERAL_TAGS,  # 通用标签列表
    BASE_TEMPLATE  # 基础模板字典
)
from core_logic import generate_salary, generate_address  # 导入生成薪资和地址的函数

fake = Faker("zh_CN")  # 创建Faker实例，用于生成中文假数据
_generated_ids = set()  # 初始化已生成的ID集合，用于确保ID唯一性


def generate_job_record() -> Dict:
    """
    生成单个职位记录（带完整性校验）
    :return: 包含职位信息的字典
    """
    job_type = _get_valid_job_type()  # 获取有效职位类型
    record = _build_base_record(job_type)  # 构建基础记录结构
    _add_dynamic_fields(record, job_type)  # 添加动态字段
    _ensure_data_integrity(record)  # 确保数据完整性
    return record  # 返回职位记录


def _get_valid_job_type() -> str:
    """
    获取有效职位类型
    :return: 随机选择的有效职位类型
    """
    return random.choice(list(TECH_REQUIREMENTS.keys()))  # 从技术要求字典的键中随机选择一个职位类型


def _build_base_record(job_type: str) -> Dict:
    """
    构建完整的基础记录结构
    :param job_type: 职位类型
    :return: 包含基础职位信息的字典
    """
    record = deepcopy(BASE_TEMPLATE)  # 深拷贝基础模板
    company_name = random.choice(BIGDATA_COMPANIES)  # 随机选择一个大数据公司

    record.update({  # 更新记录字典
        "companyFullName": company_name,  # 公司全称
        "companyShortName": _generate_short_name(company_name),  # 公司简称
        "companyType": random.choice(["上市公司", "独角兽", "行业龙头", "创业公司"]),  # 公司类型
        "financeStage": random.choice(["已上市", "D轮及以上", "C轮", "B轮", "A轮", "天使轮"]),  # 融资阶段
        "companySize": random.choice(["100-499人", "500-999人", "1000-9999人", "10000人以上"]),  # 公司规模
        "industryField": random.choice(INDUSTRY_FIELDS),  # 行业领域
        "businessArea": random.sample(INDUSTRY_FIELDS, k=random.randint(1, 3)) if random.random() > 0.1 else None,
        # 业务领域（10%概率为空）
        "workAddress": generate_address(),  # 工作地址
        "positionName": f"{job_type}工程师",  # 职位名称
        "firstType": job_type,  # 职位类型
        "education": random.choice(["本科", "硕士", "博士"]) if random.random() > 0.05 else None,  # 学历（5%概率为空）
        "workYear": f"{random.randint(1, 3)}-{random.randint(4, 8)}年" if random.random() > 0.05 else None,
        # 工作年限（5%概率为空）
        "salary": generate_salary(job_type, company_name),  # 薪资（传入公司名称）
        "jobDescription": f"负责{job_type}相关工作，包括：{_generate_job_description(job_type)}",  # 职位描述
        "positionId": _generate_unique_id(),  # 职位ID
        "formatCreateTime": fake.date_between(start_date="-1y").isoformat()  # 创建时间
    })
    return record  # 返回基础记录


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
    return name_map.get(company_name, company_name[:4] + "数据")  # 返回公司简称


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
    return "、".join(random.sample(descriptions[job_type], 3))  # 返回随机选择的职位描述


def _generate_unique_id() -> int:
    """
    生成唯一ID（防止冲突）
    :return: 唯一的ID
    """
    while True:
        new_id = random.randint(10 ** 6, 10 ** 7)  # 生成一个随机ID
        if new_id not in _generated_ids:  # 检查ID是否唯一
            _generated_ids.add(new_id)  # 添加到已生成ID集合
            return new_id  # 返回唯一ID


def _ensure_data_integrity(record: Dict):
    """
    数据完整性校验
    :param record: 包含职位信息的字典
    """
    # 强制字段校验
    mandatory_fields = ["positionId", "companyFullName", "positionName"]
    for field in mandatory_fields:
        if not record.get(field):
            raise ValueError(f"关键字段缺失: {field}")  # 抛出字段缺失异常

    # 薪资格式校验
    if "-" not in record["salary"]:
        record["salary"] = "8k-20k"  # 设置默认薪资范围
