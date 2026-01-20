#
# import json
# import logging
# import pytest
# from res import config1, config2, execute_api, extract_orderid_with_jsonpath, replace_orderid_with_regex
#
# # 配置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
# # 定义测试函数
# @pytest.mark.login
# def test_report_successful():
#     # 第一个请求
#     url1 = "http://117.72.72.134:8080/gateway/mcp/outChannel/validate?c=WI"
#     payload1 = config1['default']['payload1']  # 从 yaml 文件中读取 payload
#     response1 = execute_api(url1, payload1)
#     #使用JSONPath技术从响应数据中提取orderId
#     orderid = extract_orderid_with_jsonpath(response1)
#     print(orderid)
#
#     update_orderid=replace_orderid_with_regex(config2,orderid)
#     # 第二个请求
#     url2 = "http://117.72.72.134:8080/gateway/mcp/outChannel/accept?c=WI"
#     payload2 = config2['default']['payload2']  # 从 yaml 文件中读取 payload
#     response_json = execute_api(url2, payload2)
#     # 断言
#     if response_json is not None:
#         assert 'policyNo' in response_json['data'], "生成的响应中包含policyNo这个key"
#         logging.info("承保成功")
#         logging.info("测试用例通过")
#     else:
#         logging.error("execute_api 返回了 None，测试失败")
#         pytest.fail("execute_api 返回了 None，测试失败")

# import json
# import logging
# import pytest
# from res import config1, config2, execute_api, extract_orderid_with_jsonpath, replace_orderid_with_regex
#
# # 配置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
#
# # 定义测试函数
# @pytest.mark.login
# def test_report_successful():
#     # 第一个请求
#     url1 = "http://117.72.72.134:8080/gateway/mcp/outChannel/validate?c=WI"
#     payload1 = config1['default']['payload1']  # 从 yaml 文件中读取 payload
#     response1 = execute_api(url1, payload1)
#
#     if response1 is None:
#         pytest.fail("第一个接口请求失败")
#
#     # 使用JSONPath技术从响应数据中提取orderId
#     orderid = extract_orderid_with_jsonpath(response1)
#     print(f"提取到的orderId: {orderid}")
#
#     if orderid is None:
#         pytest.fail("无法提取orderId")
#
#     # 使用正则替换config2中的orderId
#     updated_config = replace_orderid_with_regex(config2, orderid)
#
#     # 第二个请求 - 使用更新后的配置
#     url2 = "http://117.72.72.134:8080/gateway/mcp/outChannel/accept?c=WI"
#     payload2 = updated_config['default']['payload2']  # 使用替换后的payload
#     response_json = execute_api(url2, payload2)
#
#     # 断言
#     if response_json is not None:
#         assert 'data' in response_json, "响应中应包含data字段"
#         assert 'policyNo' in response_json['data'], "生成的响应中包含policyNo这个key"
#         logging.info("承保成功")
#         logging.info("测试用例通过")
#     else:
#         logging.error("execute_api 返回了 None，测试失败")
#         pytest.fail("execute_api 返回了 None，测试失败")

import json
import logging
import pytest

from res import execute_api, replace_orderid_with_regex, config2, config1, extract_orderid_with_jsonpath

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 定义测试函数
@pytest.mark.login
def test_report_successful():
    # 第一个请求
    url1 = "http://117.72.72.134:8080/gateway/mcp/outChannel/validate?c=WI"
    payload1 = config1['default']['payload1']  # 从 yaml 文件中读取 payload
    response1 = execute_api(url1, payload1)

    if response1 is None:
        pytest.fail("第一个接口请求失败")

    # 使用JSONPath技术从响应数据中提取orderId
    orderid = extract_orderid_with_jsonpath(response1)
    print(f"提取到的orderId: {orderid}")

    if orderid is None:
        pytest.fail("无法提取orderId")

    # 调试：打印替换前的配置
    print("=== 替换前配置 ===")
    print(f"原始orderId: {config2['default']['payload2']['data']['orderId']}")

    # 使用正则替换config2中的orderId
    updated_config = replace_orderid_with_regex(config2, orderid)

    # 调试：打印替换后的配置
    print("=== 替换后配置 ===")
    print(f"新orderId: {updated_config['default']['payload2']['data']['orderId']}")

    # 检查替换是否成功
    if updated_config['default']['payload2']['data']['orderId'] == orderid:
        print("✅ orderId替换成功")
    else:
        print("❌ orderId替换失败")
        pytest.fail("orderId替换失败")

    # 第二个请求 - 使用更新后的配置
    url2 = "http://117.72.72.134:8080/gateway/mcp/outChannel/accept?c=WI"
    payload2 = updated_config['default']['payload2']  # 使用替换后的payload

    # 调试：打印实际发送的payload
    print("=== 实际发送的payload ===")
    print(json.dumps(payload2, ensure_ascii=False, indent=2))

    response_json = execute_api(url2, payload2)

    # 断言
    if response_json is not None:
        print("第二个接口请求成功")
        if 'data' in response_json:
            if 'policyNo' in response_json['data']:
                logging.info(f"承保成功，保单号: {response_json['data']['policyNo']}")
                logging.info("测试用例通过")
            else:
                logging.error("响应中未找到policyNo字段")
                logging.error(f"完整响应: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
                pytest.fail("生成的响应中不包含policyNo这个key")
        else:
            logging.error("响应中未找到data字段")
            pytest.fail("响应中应包含data字段")
    else:
        logging.error("第二个接口请求失败，返回了None")
        pytest.fail("execute_api 返回了 None，测试失败")