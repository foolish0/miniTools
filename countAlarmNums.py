import requests

# 定义请求头
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjo3NDA4LCJ1c2VyX2tleSI6Ijc0MDg6ZmViMTU1NjUtOTM4Zi00OWU4LThjMjQtNzNlMzA0MzIyMmQ2IiwidXNlcm5hbWUiOiJzaGVudGVuZyJ9.NOzG5eVbhdIDYJzNhL9NOICizuSSvSy_cVtbpMvBzrpKi6D4VZaMivWJTKRdAny3DvHMnmu_nSx6kVVGMrNwZQ'
}

# 获取stationId列表
permission_ids_url = 'http://120.25.246.122:8088/api/ego/station/permission-ids'
response = requests.get(permission_ids_url, headers=headers)
station_ids = response.json()['data']

# 初始化total计数器
total_count = 0

# 遍历stationId列表，获取每个stationId的警告数据
warnings_url = 'https://www.emind2000.cloud/rest-api/getWarnings'
for station_id in station_ids:
    params = {'stationId': station_id}
    response = requests.get(warnings_url, headers=headers, params=params)
    response_data = response.json()

    # 检查返回的code是否为200
    if response_data['code'] != 200:
        print(f"Request for stationId {station_id} failed with response: {response_data}")
        continue

    data = response_data['data']
    total_count += data['offlineAlert']['total']
    total_count += data['unplannedOperation']['total']

print(f"所有stationId下的所有数据总数为: {total_count}")