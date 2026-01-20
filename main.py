import logging
import pytest
import os
#from jsonpath import jsonpath

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("开始运行测试用例")

    # 使用相对路径指定报告路径
    report_path = "report"
    logging.info(f"报告路径为：{report_path}")

    # 确保报告路径存在
    if not os.path.exists(report_path):
        os.makedirs(report_path)
        logging.info(f"创建了报告路径：{report_path}")

    # 运行测试用例并生成 Allure 报告
    result_path = os.path.join(report_path, "result")
    pytest.main([
        "test_py.py",
        "--alluredir", result_path,
        "--clean-alluredir"  # 清理 allure 结果目录
    ])
    logging.info("测试用例运行完成")

    # 提示查看用户报告 - 使用原始字符串
    logging.info(f"Allure 报告已生成在 {result_path} 目录中。")
    logging.info("运行以下命令查看报告：")
    #logging.info(r'cd /d "D:\新框架代码\xunlianying\allure-2.34.0\bin" && allure.bat serve "D:\新框架代码\xunlianying\python\report\result"')

    logging.info(r'& "..\allure-2.34.0\bin\allure.bat" serve "report\result"')