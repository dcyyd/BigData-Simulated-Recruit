import importlib

"""
模块名称：main.py
模块职责：主程序入口和流程控制
作者：D.C.Y.
创建时间：2025/03/14 15:32:12
最后修改时间：2025/03/22 1:34:45
版本：1.0.2
版权所有 © 2025 D.C.Y. 保留所有权利
"""


def main():
    """
    主执行函数
    """
    print("请选择数据生成方式：")
    print("1. 数据生成器 --> HDFS")
    print("2. 数据生成器 --> Windows")

    choice = input("请输入你的选择（1 或 2）：")

    if choice == '1':
        run_module('generate_data_to_upload_to_hdfs')
    elif choice == '2':
        run_module('generate_data_to_windows')
    else:
        print("无效的选择，请输入 1 或 2。")


def run_module(module_name: str):
    """
    运行指定模块的主函数
    :param module_name: 模块名称
    """
    try:
        module = importlib.import_module(module_name)
        module.main()
    except ImportError:
        print(f"无法导入 {module_name} 模块，请检查文件是否存在。")
    except Exception as e:
        print(f"执行 {module_name} 时出错：{e}")


if __name__ == "__main__":
    main()
