import os

ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", "9200")
ES_USER = os.getenv("ES_USER")
ES_PWD = os.getenv("ES_PWD")
ES_INDEX = os.getenv("ES_INDEX", "platsannons-read")
ES_TAX_INDEX = os.getenv("ES_TAX_INDEX", "taxonomy")

URL_ENRICH_TEXTDOCS_BINARY_SERVICE = \
    os.getenv('URL_ENRICH_TEXTDOCS_BINARY_SERVICE',
              'https://textdoc-enrichments.dev.services.jtech.se'
              '/enrichtextdocumentbinary')
API_KEY_ENRICH_TEXTDOCS = os.getenv('API_KEY_ENRICH_TEXTDOCS')
