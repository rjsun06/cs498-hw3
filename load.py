from google.cloud import bigtable
import pandas as pd
from tqdm import tqdm
from info import *

client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
table = instance.table(table_id)
df = pd.read_csv(csv_path)

for _, row in tqdm(df.iterrows(),total=df.shape[0]):
    row_key = str(row['DOL Vehicle ID']).encode()
    row_data = table.row(row_key)
    row_data.set_cell('ev_info', 'make', str(row.get('Make', '')))
    row_data.set_cell('ev_info', 'model', str(row.get('Model', '')))
    row_data.set_cell('ev_info', 'model year', str(row.get('Model Year', '')))
    row_data.set_cell('ev_info', 'electric range', str(row.get('Electric Range', '')))
    row_data.set_cell('ev_info', 'city', str(row.get('City', '')))
    row_data.set_cell('ev_info', 'county', str(row.get('County', '')).encode('utf-8'))
    row_data.commit()