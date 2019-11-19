import logging
import requests
import certifi
import json
from ssl import create_default_context
from elasticsearch import Elasticsearch
from e2tg import settings

log = logging.getLogger(__name__)
log.info("Using Elasticsearch node at %s:%s" % (settings.ES_HOST, settings.ES_PORT))

if settings.ES_USER and settings.ES_PWD:
    context = create_default_context(cafile=certifi.where())
    elastic = Elasticsearch([settings.ES_HOST], port=settings.ES_PORT,
                            use_ssl=True, scheme='https',
                            ssl_context=context,
                            http_auth=(settings.ES_USER, settings.ES_PWD))
else:
    elastic = Elasticsearch([{'host': settings.ES_HOST, 'port': settings.ES_PORT}])


def load_groups_for_occupations(occupations, number_of_groups=3):
    relations = dict()
    for occupation in occupations:
        relations[occupation] = _get_groups(occupation, number_of_groups)
    return relations


def get_occupations_from_text(headline, text):
    # Get occupations from textdocenrich
    header = {
        'api-key': settings.ENRICH_APIKEY,
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {"doc_headline": headline, "doc_text": text}
    r = requests.post(url=settings.ENRICH_URL, headers=header,
                      json=payload)
    r.raise_for_status()

    return r.json()


def _get_groups(occupation, number_of_gropus):
    aggs_dsl = {
        "from": 0,
        "size": 0,
        "query": {
            "term": {
                "keywords.enriched.occupation.raw": occupation
            }
        },
        "aggs": {
            "groups": {
                "terms": {
                    "field": "occupation_group.concept_id.keyword",
                    "size": number_of_gropus
                }
            }
        }
    }
    es_result = elastic.search(index=settings.ES_INDEX, body=aggs_dsl)
    aggs_results = es_result.get('aggregations', {}).get('groups', {}).get('buckets', [])
    for r in aggs_results:
        g = _load_group_data(r.get('key'))
        r['concept_id'] = g['concept_id']
        r['taxonomy_id'] = g['legacy_ams_taxonomy_id']
        r['label'] = g['label']
        r['description'] = g['description']
        r['parent'] = g['parent']
        del r['key']

    return aggs_results


def _load_group_data(concept_id):
    group = elastic.get(index=settings.ES_TAX_INDEX, id=concept_id)
    return group.get('_source')


if __name__ == '__main__':
    enrichments = get_occupations_from_text("Systemutvecklare", "Vi letar efter en vass javautvecklare. Du ska vara noggrann, snabb och trevlig. Du ska kunna Java, Python, AngularJS och Cobol. Du kommer att jobba på vårt kontor i Ystad. Huvudkontoret ligger i Kiruna")
    occupations = [o['term'] for o in enrichments.get('enriched_candidates', {}).get('occupations', [])]
    results = load_groups_for_occupations(occupations, 5)
    print(json.dumps(results, indent=2))

