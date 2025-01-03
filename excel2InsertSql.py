import pandas as pd
from datetime import datetime


def excel_to_sql_insert(excel_file, table_name):
    # 读取Excel文件
    df = pd.read_excel(excel_file)

    # 获取列名
    columns = df.columns.tolist()

    # 存储SQL语句
    sql_statements = []

    # 遍历每一行数据
    for _, row in df.iterrows():
        values = []
        for col in columns:
            value = row[col]

            # 处理空值
            if pd.isna(value):
                values.append('NULL')
            # 处理日期类型
            elif isinstance(value, (pd.Timestamp, datetime)):
                values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
            # 处理字符串类型
            elif isinstance(value, str):
                values.append(f"'{value}'")
            # 处理其他类型
            else:
                values.append(str(value))

        # 生成INSERT语句
        columns_str = ', '.join(columns)
        values_str = ', '.join(values)
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
        sql_statements.append(sql)

    return sql_statements


def main():
    # 使用示例
    excel_file = '/Users/lizhenjiang/Desktop/项目交付台账-表格全文.xlsx'  # Excel文件路径
    table_name = 'project_delivery_ledger_copy1'  # 数据库表名

    try:
        sql_statements = excel_to_sql_insert(excel_file, table_name)

        # 将SQL语句写入文件
        with open('output.sql', 'w', encoding='utf-8') as f:
            for sql in sql_statements:
                f.write(sql + '\n')

        print(f"成功生成SQL语句，已保存到 output.sql 文件中")

    except Exception as e:
        print(f"发生错误: {str(e)}")


if __name__ == '__main__':
    main()