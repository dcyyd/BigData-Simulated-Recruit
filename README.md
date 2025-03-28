<div align="center">
  <h1>🔥 BigData-Simulated-Recruit</h1>
  <p>大数据行业招聘数据生成器</p>
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg?logo=creative-commons" alt="License">  <!-- 更新许可证徽章 -->
  <img src="https://img.shields.io/badge/DataScale-30MB%2F30kRecords-orange" alt="DataScale">
</div><br/>


> 🚀 **简&nbsp;&nbsp;&nbsp;介**：高度仿真的大数据行业招聘数据生成器 | 支持压力测试/算法训练/行业研究  
> 📅 **版&nbsp;&nbsp;&nbsp;本**：v1.0.0 | 最后更新：2025-03-21  
> 👨 **开发者**：D.C.Y. 窦长友 | © 2025 D.C.Y. Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

![img.png](img.png)

### 🌟 核心特性

- **全维度数据模拟**  
  📊 覆盖企业信息/岗位要求/薪资体系/技术标签等20+关键维度  
  🏙️ 支持一二三线城市特征分布  
  💰 动态薪资模型（参考《2025中国薪酬白皮书》）


- **行业级标准规范**  
  ✅ GB/T 35295-2017 大数据术语规范  
  📜 JSON Schema Draft-07 数据结构  
  🧮 数据缺失率<5%模拟真实场景


- **高性能生成引擎**  
  ⚡ 单文件生成<500ms | 30MB数据量  
  🧠 内存优化算法（峰值<50MB）  
  🔄 支持横向扩展至百万级数据



### 🛠️ 快速开始

- **环境准备**
    ```bash
    # 克隆仓库
    git clone https://github.com/dcyyd/BigData-Simulated-Recruit.git
    
    # 进入项目目录
    cd BigData-Simulated-Recruit/src
    
    # 创建虚拟环境
    python -m venv xenv
    
    # 激活环境
    source xenv/bin/activate  # Linux/Mac
    xenv\Scripts\activate.bat  # Windows
    
    # 安装依赖
    pip install -r requirements.txt
    ```

-  **数据生成**
    ```python
    # 运行生成器
    python main.py
    ```
- **成功输出样例**
    ```markdown
    模拟数据生成完毕，共生成30个文件，每个文件包含1000条记录
    ```
- **项目打包**
    ```bash
    # 安装打包工具
    pip install setuptools wheel
    # 执行打包命令
    python setup.py sdist bdist_wheel
    ```
- **打包成功**

  打包完成后会在项目根目录生成：

    ```markdown
    dist/ 目录：包含.tar.gz源码包和.whl二进制包
    build/ 目录：临时构建文件
    项目名称.egg-info：项目元数据
    ```

### 📂 项目结构
```markdown
BigData-Simulated-Recruit/
├── JobData/               # 无扩展名数据文件
│   └── page1...page30     
├── JobData-Json/          # JSON格式数据文件
│   └── page1.json...page30.json
├── src/                  # 核心源码目录
│   ├── core_logic.py     # 薪资地址生成逻辑
│   ├── data_definitions.py # 数据定义
│   ├── data_generation.py # 数据生成逻辑
│   ├── generate_data_to_upload_to_hdfs.py # 数据生成器--> HDFS
│   ├── generate_data_to_windows.py # 数据生成器--> windows
│   └── main.py           # 主程序入口
├── requirements.txt      # 项目依赖
├── .gitignore            # Git忽略文件
├── setup.py              # 项目配置文件
├── LICENSE               # 项目许可证
├── README.md              # 项目文档
└── README_en.md           # 英文版项目文档
```

### 📊 数据样本

```json
{
  "companyFullName": "腾讯大数据中心",
  "positionName": "数据科学家工程师",
  "salary": "45k-60k",
  "workAddress": "深圳南山区科技园27栋",
  "requirements": [
    {
      "一级要求": "技术能力",
      "二级要求": ["精通统计学和机器学习算法", "能够使用R语言进行数据分析"]
    },
    {
      "一级要求": "业务理解", 
      "二级要求": ["有实际业务场景中的数据挖掘经验"]
    }
  ],
  "positionLables": ["深度学习", "因果推断", "大数据行业", "人工智能融合"]
}
```

### ⚙️ 技术架构
```mermaid
graph TD
    A[用户选择数据生成方式] --> B{选择1或2?}
    B -->|1. 生成到HDFS| C[初始化HDFS模块]
    B -->|2. 生成到Windows| D[初始化Windows模块]

    subgraph HDFS流程
        C --> E[清空历史目录]
        C --> F[创建存储目录]
        C --> G[循环生成30文件]
        G --> H[数据生成引擎]
    end

    subgraph Windows流程
        D --> I[创建本地目录]
        D --> J[循环生成30文件]
        J --> H
    end

    subgraph 核心数据生成
        H --> K[生成批量数据\n1000条/文件]
        K --> L[调用generate_job_record]
        L --> M[生成新资源库]
        L --> N[生成地址源库]
        L --> O[基础数据模板]
        K --> P[数据校验]
        P --> Q[格式自动修复]
    end

    subgraph 存储操作
        HDFS流程 --> R[上传HDFS\n/JobData/日期目录]
        Windows流程 --> S[保存本地\n../JobData*]
    end

    style A fill:#FFD700,stroke:#333,color:#2F4F4F
    style B fill:#87CEEB,stroke:#333,color:#2F4F4F
    style C fill:#98FB98,stroke:#333,color:#006400
    style D fill:#98FB98,stroke:#333,color:#006400
    style H fill:#FFA07A,stroke:#333,color:#8B0000
    style K fill:#DDA0DD,stroke:#333,color:#4B0082
    style P fill:#FF6347,stroke:#333,color:#FFFFFF
    style R fill:#20B2AA,stroke:#333,color:#FFFFFF
    style S fill:#20B2AA,stroke:#333,color:#FFFFFF

    classDef user fill:#FFD700,stroke:#333,color:#2F4F4F;
    classDef branch fill:#87CEEB,stroke:#333,color:#2F4F4F;
    classDef module fill:#98FB98,stroke:#333,color:#006400;
    classDef process fill:#FFA07A,stroke:#333,color:#8B0000;
    classDef data fill:#DDA0DD,stroke:#333,color:#4B0082;
    classDef verify fill:#FF6347,stroke:#333,color:#FFFFFF;
    classDef storage fill:#20B2AA,stroke:#333,color:#FFFFFF;

    class A user
    class B branch
    class C,D module
    class H process
    class K data
    class P verify
    class R,S storage
```

### 🚫数据免责声明
- **许可协议**：本项目采用<a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank">知识共享署名-非商业性使用 4.0 国际许可协议</a> 进行许可。
- **项目用途**：本项目生成的数据仅用于学习和研究目的，允许非商业性使用，但请保留版权信息。
- **企业信息**：全量数据通过算法生成，与现实企业无任何关联
- **薪资体系**：基于虚拟经济模型构建，不反映真实薪资水平
- **地理坐标**：地址信息采用模板化生成，无真实地理位置映射 
- **技术标签**：标签信息通过算法生成，与真实技术标签无关联
- **合规保障**：
  - 严格遵循GB/T 35295-2017大数据术语规范
  - 数据结构符合JSON Schema Draft-07标准
  - 生成过程符合GDPR匿名化要求

### 🤝 贡献指南
欢迎通过以下方式参与贡献：

- **问题反馈**：在GitHub提交Issue说明问题
- **代码提交**：
  - Fork仓库并创建特性分支（`feat/xxx`）
  - 遵循PEP8代码规范，提交清晰的Commit Message
  - 发起Pull Request并关联相关Issue
- **文档改进**：完善文档或翻译版本
- **协议限制**：禁止将本项目用于商业用途（遵循<a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank">CC BY-NC 4.0</a>）

### 📜项目日志
- (v1.0.0 | 2025-03-14 | 初始版本发布)
- (v1.0.1 | 2025-03-21 | 修复数据生成逻辑)
- (v1.0.2 | 2025-03-22 | 优化数据生成逻辑)

### 📮 联系我们

- 📧 **项目维护**：**D.C.Y.** <a href="mailto:dcyyd_kcug@yeah.net">dcyyd_kcug@yeah.net</a><br>
- 🌐 **个人主页**：<a href="https://dcyyd.github.io" target="_blank">https://dcyyd.github.io</a>