import pymysql
import requests
import json

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

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

def get_job_nums(usernames, url, access_token):
    full_url = f"{url}?access_token={access_token}"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "open_userid_list": usernames,
        "source_agentid": 1000212
    }
    response = requests.post(full_url, json=body, headers=headers)
    data = response.json()

    if data["errcode"] != 0:
        raise Exception(f"Error: {data['errmsg']}")

    return {item["open_userid"]: item["userid"] for item in data["userid_list"]}

def generate_and_execute_update_statements(config_path):
    config = load_config(config_path)
    db_config = config['db_config']
    url = config['url']
    access_token = config['access_token']

    usernames = get_usernames_from_db(db_config)
    job_nums = get_job_nums(usernames, url, access_token)
    update_statements = []

    conn = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    cursor = conn.cursor()

    success_count = 0
    failure_count = 0
    failed_statements = []

    for username in usernames:
        if username in job_nums:
            job_num = job_nums[username]
            update_statement = f"UPDATE sys_jdy_user SET job_num = '{job_num}' WHERE username = '{username}';"
            update_statements.append(update_statement)
            print(update_statement)
            try:
                cursor.execute(update_statement)
                success_count += 1
            except Exception as e:
                failure_count += 1
                failed_statements.append(update_statement)
                print(f"Failed to execute: {update_statement}, Error: {e}")

    conn.commit()
    conn.close()

    print(f"Successfully executed: {success_count} statements")
    print(f"Failed to execute: {failure_count} statements")
    if failed_statements:
        print("Failed statements:")
        for statement in failed_statements:
            print(statement)

    return update_statements

# 示例使用
config_path = 'config/config.json'
generate_and_execute_update_statements(config_path)