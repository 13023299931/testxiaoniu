
import requests
import json
import random
import yaml
import logging
from excel import read_excel_value

# 获取日志记录器对象
logger = logging.getLogger(__name__)

# 创建日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取 Excel 文件中的路径
file_path = r'C:\Users\86130\Desktop\xunlianying\python\case\A1000013.xlsx'
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
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    response_json = None  # 初始化 response_json 为 None

    if response.status_code == 200:
        logging.info('请求成功')
        logging.info('请求URL: ' + response.request.url)
        logging.info('请求报文: ' + str(response.request.body))

        response_text1 = response.text
        response_text2 = response.text

        response_json1 = json.loads(response_text1)
        response_json2 = json.loads(response_text2)

        if 'orderId' in response_json1['data']:
            orderId = response_json1['data']['orderId']
            logging.info("响应报文为:" + response_text1)
            logging.info("生成的订单号为:" + orderId)

        if 'policyNo' in response_json2['data']:
            policyNo = response_json2['data']['policyNo']
            logging.info("响应报文为:" + str(response_text2))
            logging.info("生成的保单号为:" + policyNo)
    else:
        logging.info('请求失败')

    return response_json2  # 返回响应报文



