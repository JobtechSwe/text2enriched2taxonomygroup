import os

ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", "9200")
ES_USER = os.getenv("ES_USER")
ES_PWD = os.getenv("ES_PWD")
ES_INDEX = os.getenv("ES_INDEX", "platsannons-read")
ES_TAX_INDEX = os.getenv("ES_TAX_INDEX", "taxonomy")

ENRICH_URL = os.getenv('ENRICH_URL',
                       'https://textdoc-enrichments.dev.services.jtech.se'
                       '/enrichtextdocumentbinary')
ENRICH_APIKEY = os.getenv('ENRICH_APIKEY')
