import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义请求头
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjozNjY4LCJ1c2VyX2tleSI6IjM2Njg6MWM5ZTZhMTctZDMwZi00YzliLWI3YjktZDY2NGYzZmI1NjA3IiwidXNlcm5hbWUiOiJ3dWppbmxhbiJ9.2vfM41r0Um_ATYXZoO8DpTiB7gFNAP4pDCPNa2fTikrbpdmekGRDVIKJmokF7hbIz0qKjGHcKU3HIxxM6nL5FQ'
}

# 获取stationId列表
permission_ids_url = 'http://120.25.246.122:8088/api/ego/station/permission-ids'
response = requests.get(permission_ids_url, headers=headers)
station_ids = response.json()['data']

# 初始化total计数器
total_count = 0
failed_station_ids = []

# 定义处理单个stationId请求的函数
def fetch_warnings(station_id):
    warnings_url = 'https://www.emind2000.cloud/rest-api/getWarnings'
    params = {'stationId': station_id}
    response = requests.get(warnings_url, headers=headers, params=params)
    response_data = response.json()

    # 检查返回的code是否为200
    if response_data['code'] != 200:
        print(f"Request for stationId {station_id} failed with response: {response_data}")
        failed_station_ids.append(station_id)
        return 0

    data = response_data['data']
    return data['offlineAlert']['total'] + data['unplannedOperation']['total']

# 使用ThreadPoolExecutor并发执行请求
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_warnings, station_id) for station_id in station_ids]
    for future in as_completed(futures):
        total_count += future.result()

print(f"所有stationId下的所有数据总数为: {total_count}")
print(f"所有返回不是200的请求参数stationId: {failed_station_ids}")