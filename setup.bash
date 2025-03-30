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

sudo apt-get install python3-venv
python3 -m venv .venv
chmod +x ./.venv/bin/activate
./.venv/bin/activate

curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

python3 -m pip install google-cloud-bigtable pandas flask tqdm

python3 load.py

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
sudo apt-get install iptables-persistent
sudo netfilter-persistent save

python3 app.py
