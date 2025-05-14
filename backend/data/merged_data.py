import pandas as pd

files = [r"C:\Users\abhi1\Desktop\Dakshina Kannada\backend\data\Dakshina Kannada 2021-06-01 to 2023-12-31.csv", r"C:\Users\abhi1\Desktop\Dakshina Kannada\backend\data\dakshina_kannada_weather.csv"]

columns_to_keep = ['datetime', 'temp', 'humidity', 'precip', 'precipprob', 'windspeed']


dfs = []
for file in files:
    df = pd.read_csv(files)
    df = df[columns_to_keep]
    df['city'] = file.split("/")[-1].replace("_weather.csv", "").capitalize()
    dfs.append(df)


combined_df = pd.concat(dfs, ignore_index=True)


combined_df.to_csv('data/Dmerged_flood_data.csv', index=False)
print("Data Merged successfully in data/Dmerged_flood_data.csv")
