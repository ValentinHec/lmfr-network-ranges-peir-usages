# lmfr-network-ranges-peir-usages

- Récupérer le script :

<code>
git clone lien
</code>

- Créer un virtual env dans le dossier du script:

<code>
mkdir venv

python3 -m venv venv
</code>

- Créer un fichier <code>.env</code> :


export IPAM_LOGIN=API_infoblox\

export IPAM_PASSWORD=AJOUTER PWD\

export IPAM_HOSTNAME=ipam.fr.corp.leroymerlin.com\


export DEFAULT_THRESHOLD_MIN_IPAM=200\

export OUTPUT_PATH="/var/www/html/lmfr-network-list-usage/"


- Pour lancer le script :

<code>
source .env

./venv/bin/python csv_peir_usage.py </code> for one csv peir usage

<code>./venv/bin/python one_csv.py</code> for a global csv

<code>./venv/bin/python export_global.py</code> for a global csv and one csv peir usage
