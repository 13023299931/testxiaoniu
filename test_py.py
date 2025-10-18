
import json
import logging
import pytest
from res import config1, config2, execute_api

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义测试函数
@pytest.mark.login
def test_report_successful():
    # 第一个请求
    url1 = "http://117.72.72.134:8080/gateway/mcp/outChannel/validate?c=WI"
    payload1 = config1['default']['payload1']  # 从 yaml 文件中读取 payload
    response1 = execute_api(url1, payload1)
    # 第二个请求
    url2 = "http://117.72.72.134:8080/gateway/mcp/outChannel/accept?c=WI"
    payload2 = config2['default']['payload2']  # 从 yaml 文件中读取 payload
    response_json = execute_api(url2, payload2)
    # 断言
    if response_json is not None:
        assert 'policyNo' in response_json['data'], "生成的响应中包含policyNo这个key"
        logging.info("承保成功")
        logging.info("测试用例通过")
    else:
        logging.error("execute_api 返回了 None，测试失败")
        pytest.fail("execute_api 返回了 None，测试失败")