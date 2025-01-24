import pymysql
import requests

def get_usernames_from_db(db_config):
    conn = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM sys_jdy_user")
    usernames = [row[0] for row in cursor.fetchall()]
    conn.close()
    return usernames

def get_job_nums(usernames, access_token):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/batch/openuserid_to_userid?access_token={access_token}"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "open_userid_list": usernames,
        "source_agentid": 1000212
    }
    response = requests.post(url, json=body, headers=headers)
    data = response.json()

    if data["errcode"] != 0:
        raise Exception(f"Error: {data['errmsg']}")

    return {item["open_userid"]: item["userid"] for item in data["userid_list"]}

def generate_update_statements(db_config, access_token):
    usernames = get_usernames_from_db(db_config)
    job_nums = get_job_nums(usernames, access_token)
    update_statements = []

    for username in usernames:
        if username in job_nums:
            job_num = job_nums[username]
            update_statements.append(f"UPDATE sys_jdy_user SET job_num = '{job_num}' WHERE username = '{username}';")

    return update_statements

# 示例使用
db_config = {
    'host': '192.168.4.80',
    'user': 'root',
    'password': '4DrveSG!jTu%',
    'database': 'data_warehouse_prod'
}
access_token = 'j9UB-RKQNcqB95S92u8sPIuQBQt8yEneFB69J0sNfW0lbMqIrExikSNXtauCW4dYHroCYZSX4Y-42w0lN4zGoUPgZBoDz2iz9ahYSA8RXprkD2zClwTcIYN-R8kdKZncNoXmZFhDhMk2g0y8CkJoqjt0iY8aQOODDQ8lqc_VZ1aqkkmkBVk7GHXPNrCZnbNWAGpU0NxyXevCWLW5YiQf9w'
update_statements = generate_update_statements(db_config, access_token)
for statement in update_statements:
    print(statement)