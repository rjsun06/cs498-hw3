sudo apt-get update
curl http://ifconfig.me

gcloud services enable bigtable.googleapis.com

gcloud bigtable instances create ev-bigtable \
    --cluster=ev-cluster \
    --cluster-zone=us-central1-a \
    --display-name="EV Bigtable" \
    --instance-type=PRODUCTION

gcloud bigtable instances tables create ev-population \
    --instance=ev-bigtable \
    --column-families=ev_info

python3 -m venv .venv
chmod +x ./.venv/bin/activate
./.venv/bin/activate

curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

python3 -m pip install google-cloud-bigtable pandas flask

python3 load.py

python3 app.py