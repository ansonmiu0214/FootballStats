import pandas as pd
from statsbombpy import sb
from sqlalchemy import create_engine
db_path = r"C:\Users\amete\OneDrive\Documents\Football Stat\instance\footballDB.db"
engine = create_engine(f'sqlite:///{db_path}')
match_df = sb.events(match_id=3857256)

# Print data types of each column
for column in match_df.columns:
    data_type = match_df[column].dtype
    print(f"{column}: {data_type}")
#match_df.to_sql('gamestats', engine, if_exists='append', index=False)
#print (match_df)