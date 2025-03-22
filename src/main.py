import importlib

"""
模块名称：main.py
模块职责：主程序入口和流程控制
作者：D.C.Y.
创建时间：2025/03/14 15:32:12
最后修改时间：2025/03/22 1:34:45
版本：1.0.2
copyright © 2025 D.C.Y. All rights reserved
"""


def main():
    print("请选择数据生成方式：")
    print("1. 数据生成器 --> HDFS")
    print("2. 数据生成器 --> Windows")

    choice = input("请输入你的选择（1 或 2）：")

    if choice == '1':
        try:
            module = importlib.import_module('generate_data_to_upload_to_hdfs')
            module.main()
        except ImportError:
            print("无法导入 generate_data_to_upload_to_hdfs 模块，请检查文件是否存在。")
        except Exception as e:
            print(f"执行 generate_data_to_upload_to_hdfs 时出错：{e}")
    elif choice == '2':
        try:
            module = importlib.import_module('generate_data_to_windows')
            module.main()
        except ImportError:
            print("无法导入 generate_data_to_windows 模块，请检查文件是否存在。")
        except Exception as e:
            print(f"执行 generate_data_to_windows 时出错：{e}")
    else:
        print("无效的选择，请输入 1 或 2。")


if __name__ == "__main__":
    main()
