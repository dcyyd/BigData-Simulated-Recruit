from setuptools import setup, find_packages

# 使用setuptools的setup函数来配置包信息
setup(
    name="bigdata_recruitment_simulator",  # 包名
    version="1.0.2",  # 版本号
    author="D.C.Y.",  # 作者
    description="Bigdata Recruitment Information Simulator",  # 简短描述
    url="https://github.com/dcyyd/BigData-Simulated-Recruit",  # 项目地址

    packages=find_packages(where="src"),  # 从src目录下查找包
    package_dir={"": "src"},  # 将src目录下的包作为根目录
    install_requires=[
        "python-dateutil>=2.8.2",  # 依赖的python-dateutil库，版本号大于等于2.8.2
        "faker>=18.11.2",  # 依赖的faker库，版本号大于等于18.11.2
    ],
    python_requires=">=3.8",  # 依赖的python版本号大于等于3.8
    classifiers=[
        "Programming Language :: Python :: 3",  # 编程语言为Python 3
        "License :: Other/Proprietary License",  # 许可证为其他私有许可证
        "License :: Free for non-commercial use",  # 非商业用途免费
        "Operating System :: OS Independent",  # 操作系统无关
    ],
)
