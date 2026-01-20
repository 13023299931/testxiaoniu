import re

import requests
import json
import random
import yaml
#from jsonpath import jsonpath

import logging
from excel import read_excel_value

# 获取日志记录器对象
logger = logging.getLogger(__name__)

# 创建日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取 Excel 文件中的路径
#绝对路径写法
#file_path = r'D:\新框架代码\xunlianying\python\case\A1000013.xlsx'
#相对路径写法
file_path = r'case\A1000013.xlsx'
value1 = read_excel_value(file_path, 2, 2)  # 第二行第二列的值
value2 = read_excel_value(file_path, 3, 2)  # 第三行第二列的值

print(value1)
print(value2)

# 读取 yaml 文件
def load_yaml_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
config1 = load_yaml_config(value1)
config2 = load_yaml_config(value2)

def execute_api(url, payload):
    headers = {'Content-Type': 'application/json'}

    try:
        logging.info(f'开始请求URL: {url}')
        logging.info(f'请求报文: {json.dumps(payload, ensure_ascii=False, indent=2)}')

        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=30)

        logging.info(f'响应状态码: {response.status_code}')
        logging.info(f'响应头: {dict(response.headers)}')

        if response.status_code == 200:
            logging.info('请求成功')

            response_text = response.text
            logging.info(f'响应正文: {response_text}')

            try:
                response_json = json.loads(response_text)

                # 检查并记录 orderId
                if 'data' in response_json and 'orderId' in response_json['data']:
                    orderId = response_json['data']['orderId']
                    logging.info("生成的订单号为:" + orderId)

                # 检查并记录 policyNo
                if 'data' in response_json and 'policyNo' in response_json['data']:
                    policyNo = response_json['data']['policyNo']
                    logging.info("生成的保单号为:" + policyNo)

                return response_json

            except json.JSONDecodeError as e:
                logging.error(f'JSON解析失败: {e}')
                logging.error(f'原始响应: {response_text}')
                return None

        else:
            logging.error(f'请求失败，状态码: {response.status_code}')
            logging.error(f'错误响应: {response.text}')
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f'请求异常: {e}')
        return None
    except Exception as e:
        logging.error(f'未知错误: {e}')
        return None



def extract_orderid_with_jsonpath(response_data):
    """
    从响应数据中提取orderId
    """
    try:
        # 直接提取 orderId，不需要 jsonpath
        if isinstance(response_data, dict) and 'data' in response_data and 'orderId' in response_data['data']:
            orderid = response_data['data']['orderId']
            logging.info(f"提取到的orderId: {orderid}")
            return orderid
        else:
            logging.warning("未找到orderId字段")
            return None
    except Exception as e:
        logging.error(f"提取orderId失败: {e}")
        return None
def replace_orderid_with_regex(yaml_config, new_orderid):
    """
    使用正则表达式替换YAML配置中的orderId
    """
    try:
        # 将YAML配置转换为字符串
        yaml_str = yaml.dump(yaml_config, allow_unicode=True)

        print(f"=== 替换前的YAML字符串 ===")
        print(yaml_str)

        # 方法1：直接使用字符串替换（最简单有效）
        if "orderId: '{{ORDER_ID}}'" in yaml_str:
            modified_yaml_str = yaml_str.replace("orderId: '{{ORDER_ID}}'", f"orderId: '{new_orderid}'")
            print("✅ 使用字符串替换成功")

        # 方法2：如果方法1没匹配，使用正则表达式
        elif '{{ORDER_ID}}' in yaml_str:
            # 匹配：orderId: 任意空白 '{{ORDER_ID}}'
            pattern = r"(orderId:\s*)'{{ORDER_ID}}'"
            matches = re.findall(pattern, yaml_str)
            print(f"正则匹配结果: {matches}")

            if matches:
                replacement = f"{matches[0]}'{new_orderid}'"
                modified_yaml_str = re.sub(pattern, replacement, yaml_str)
                print("✅ 使用正则替换成功")
            else:
                modified_yaml_str = yaml_str
                print("❌ 正则未匹配到模式")
        else:
            modified_yaml_str = yaml_str
            print("❌ 未找到{{ORDER_ID}}占位符")

        print(f"=== 替换后的YAML字符串 ===")
        print(modified_yaml_str)

        # 检查替换是否真的发生了
        if '{{ORDER_ID}}' in modified_yaml_str:
            print("❌ 替换未生效，{{ORDER_ID}}仍然存在")
        else:
            print("替换已生效，{{ORDER_ID}}已被替换")

        # 将修改后的YAML字符串转换回字典
        modified_config = yaml.safe_load(modified_yaml_str)
        return modified_config

    except Exception as e:
        logging.error(f"正则替换失败: {e}")
        return yaml_config