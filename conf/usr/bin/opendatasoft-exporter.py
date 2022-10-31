from prometheus_client import start_http_server, CollectorRegistry
from prometheus_client.core import GaugeMetricFamily
import requests
from datetime import datetime, timedelta
import requests
import signal

REG = CollectorRegistry()

metrics = [
    "ech_comm_suisse", 
    "consommation", 
    "fioul_cogen", 
    "eolien", 
    "bioenergies_dechets", 
    "ech_physiques", 
    "fioul_tac", 
    "charbon", 
    "bioenergies", 
    "nucleaire", 
    "ech_comm_angleterre", 
    "gaz_ccg", 
    "ech_comm_allemagne_belgique", 
    "hydraulique_step_turbinage", 
    "gaz", 
    "solaire", 
    "stockage_batterie", 
    "hydraulique", 
    "fioul_autres", 
    "taux_co2", 
    "gaz_cogen", 
    "destockage_batterie", 
    "pompage", 
    "bioenergies_biomasse", 
    "bioenergies_biogaz", 
    "fioul", 
    "eolien_offshore", 
    "ech_comm_italie", 
    "gaz_tac", 
    "ech_comm_espagne", 
    "gaz_autres", 
    "hydraulique_lacs", 
    "eolien_terrestre", 
    "hydraulique_fil_eau_eclusee"
]

# Decorate function with metric.

class Collector:


    def collect(self):
        args = {
            "dataset": "eco2mix-national-tr",
            "q": [
                f"date_heure>={(datetime.now() - timedelta(hours = 2)).strftime('%Y-%m-%dT%H:00:00.00')}",
                f"date_heure<={(datetime.now() - timedelta(hours = 1)).strftime('%Y-%m-%dT%H:00:00.00')}"
            ],
            "rows": 1,
            "start": 3,
            "sort": "date_heure"
        }
        ret = requests.get("https://odre.opendatasoft.com/api/records/1.0/search/", args)
        try:
            data = ret.json()["records"][0]["fields"]
            for metric in metrics:
                if metric in data and data[metric] != "ND":
                    yield GaugeMetricFamily(f'opendatasoft_{metric}', '', value=data[metric])
        except:
            pass

if __name__ == '__main__':
    REG.register(Collector())
    start_http_server(9100, registry=REG)
    signal.pause()
   