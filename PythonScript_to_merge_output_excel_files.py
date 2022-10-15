import os
import pandas as pd


data_file_folder='/home/ubuntu/excel'

df = []

for file in os.listdir(data_file_folder):
    if file.endswith('.xlsh'):
        print('Loading file {0}...'.format(file))
        df.append(pd.read_excel(os.path.join(data_file_folder, file), sheet_name='Emails'))


df_master= pd.concat(df, axis=0)
df_master.to_excel('master_file.xlsh', index=False)
