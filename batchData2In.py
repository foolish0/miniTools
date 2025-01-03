data_string = """18c57b856638bdebbb4e4534d32b2384
18cd71213e2e1bb986a9a7b4cb7b3a35
18f65bd8c4c2fc1b1368190446f8371b
18f89927ec8d08f2d7ca762433b83891
19071d1bf7df4c0402cb3ca4f5dae380
1918f24aff75fb4014b5c2643daa2ce7
191c16dd312549bf4fbf0784b919a968
191db6bbb9cbeb94cf77eb440a2bfa64
19332a69c12c2130b73875d4f4885eb0
19332bbed3e79a18a3575cd46fbbcedd
19332bf1b052fd9091bbf5a478594db5
193aacc873afec784d24909407ab6bc6
193b8bd4fc55477024f04b24dd8968ff
193d93fa00c3d962d781f1f4b508b787"""

data_list = data_string.split('\n')
sql_in_condition = ", ".join([f"'{item}'" for item in data_list])
sql_query = f"IN ({sql_in_condition})"

print(sql_query)