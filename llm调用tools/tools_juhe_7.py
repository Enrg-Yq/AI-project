import requests

# 41-外汇汇率 - 代码参考（根据实际业务情况修改）

# 基本参数配置
apiUrl = 'http://web.juhe.cn/finance/exchange/frate'  # 接口请求URL
apiKey = 'eb6bee402bb44eed82ece22711ee30a1'  # 在个人中心->我的数据,接口名称上方查看

# 接口请求入参配置
requestParams = {
    'key': apiKey,
    'type': '',
}

# 发起接口网络请求
response = requests.get(apiUrl, params=requestParams)

# 解析响应结果
if response.status_code == 200:
    responseResult = response.json()
    # 网络请求成功。可依据业务逻辑和接口文档说明自行处理。
    print(responseResult)
else:
    # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
    print('请求异常')