
import logging
import pytest
import os

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("开始运行测试用例")

    # 指定报告路径
    report_path = r"C:\Users\86130\Desktop\xunlianying\python\report"

    logging.info(f"报告路径为：{report_path}")

    # 确保报告路径存在
    if not os.path.exists(report_path):
        os.makedirs(report_path)
        logging.info(f"创建了报告路径：{report_path}")

    # 运行测试用例并生成 Allure 报告
    # 定义 Allure 结果的存储路径
    report_path = os.path.join(report_path, "result")
    pytest.main([
        r"C:\Users\86130\Desktop\xunlianying\python\test_py.py",  # 使用绝对路径
        "--alluredir", report_path  # 指定 Allure 报告的存储路径
    ])
    logging.info("测试用例运行完成")

    # 提示查看用户报告
    logging.info(f"Allure 报告已生成在 {report_path} 目录中。")
    logging.info("运行以下命令查看报告：")
    logging.info(f"allure serve {report_path}")