
from flask import current_app
import requests

from authoraffsrv.client import client

def get_solr_data(bibcodes, cutoff_year, start=0, sort='date desc'):
    data = 'bibcode\n' + '\n'.join(bibcodes)

    rows = min(current_app.config['AUTHOR_AFFILATION_SERVICE_MAX_RECORDS_SOLR'], len(bibcodes))

    query = 'year >= "' + str(cutoff_year) + '"'

    fields = 'author,aff,pubdate'

    params = {
        'q': query,
        'wt': 'json',
        'rows': rows,
        'start': start,
        'sort': sort,
        'fl': fields,
        'fq': '{!bitset}'
    }

    headers = {'Authorization':'Bearer '+current_app.config['AUTHOR_AFFILIATION_SERVICE_ADSWS_API_TOKEN']}

    try:
        response = client().post(
            url=current_app.config['AUTHOR_AFFILIATION_SOLRQUERY_URL'],
            params=params,
            data=data,
            headers=headers
        )
        if (response.status_code == 200):
            return response.json()
        return None
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        current_app.logger.error('Solr exception. Terminated request.')
        current_app.logger.error(e)
        return None

