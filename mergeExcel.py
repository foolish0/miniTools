import pandas as pd
import os

path = "/Users/lizhenjiang/Desktop/储能备案项目_副本"  # 修改为你的文件夹路径
all_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.xlsx')]

combined_df = pd.DataFrame()

for file in all_files:
    df = pd.read_excel(file)
    combined_df = pd.concat([combined_df, df], ignore_index=True)

combined_df.to_excel("combined_file.xlsx", index=False)