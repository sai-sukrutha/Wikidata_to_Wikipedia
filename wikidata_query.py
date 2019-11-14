import requests
import json

wikidata_sparql_url = "https://query.wikidata.org/sparql"
wikidata_url = "https://www.wikidata.org/w/api.php"


def get_qnumber(wikiarticle, wikisite):
    resp = requests.get(wikidata_url, {
        'action': 'wbgetentities',
        'titles': wikiarticle,
        'sites': wikisite,
        'props': '',
        'format': 'json'
    }).json()
    return list(resp['entities'])[0]


def run_query(query):
    try:
        res = requests.get(wikidata_sparql_url,params={'format': 'json','query':query})
        res = res.json()
    except json.JSONDecodeError as e:
        raise Exception('Invalid query')
        print("Invalid query")
        return NULL
    return res
