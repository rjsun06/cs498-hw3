from flask import Flask
from google.cloud import bigtable
from info import *
app = Flask(__name__)

client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
table = instance.table(table_id)

@app.route('/rows')
def rows():
    count = 0
    for _ in table.read_rows():
        count += 1
    return str(count)

@app.route('/Best-BMW')
def best_bmw():
    count = 0
    for row in table.read_rows():
        try:
            count += \
            (row.cells['ev_info'].get(b'make', [None])[0].value.decode().lower() == 'bmw') \
            and \
            (int(row.cells['ev_info'].get(b'electric range', [None])[0].value.decode()) > 100)
        except:
            continue
    return str(count)

@app.route('/tesla-owners')
def tesla_owners():
    count = 0
    for row in table.read_rows():
        try:
            make = row.cells['ev_info'].get(b'make', [None])[0].value.decode().lower()
            city = row.cells['ev_info'].get(b'city', [None])[0].value.decode().lower()
            if make == 'tesla' and city == 'seattle':
                count += 1
        except:
            continue
    return str(count)

@app.route('/update')
def update():
    row = table.row('257246118'.encode())
    row.set_cell('ev_info', 'electric range', '200')
    row.commit()
    return "Success"

@app.route('/delete')
def delete():
    to_delete = []
    for row in table.read_rows():
        try:
            model_year = row.cells['ev_info'].get(b'model year', [None])[0].value.decode()
            if model_year < 2014:
                to_delete.append(row.row_key)
        except:
            continue
    for key in to_delete:
        row = table.row(key)
        row.delete()
        row.commit()
    return rows()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)