# -*- coding: utf-8 -*-

import sys
import os
PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(PROJECT_HOME)

from flask_testing import TestCase
import unittest

import authoraffsrv.app as app
from authoraffsrv.tests.unittests.stubdata import solrdata, formatted, export
from authoraffsrv.views import Formatter, Export, EXPORT_FORMATS, is_number

class TestAuthorAffiliation(TestCase):
    def create_app(self):
        """
        start the wsgi application

        """
        return app.create_app()

    def test_formatted_data(self):
        """
        general test

        """
        # format the stubdata using the code
        formatted_data = Formatter(solrdata.data).get(0, 2017)
        # now compare it with an already formatted data that we know is correct
        assert(formatted_data == formatted.data)

    def test_solr_status_error(self):
        """
        when solr returns error

        """
        solr_data = {
           "responseHeader":{
              "status":400,
              }
           }
        formatted_data = Formatter(solr_data).get()
        assert(formatted_data == None)

    def test_export_csv_format(self):
        """
        csv format test

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).format(EXPORT_FORMATS[0])
        # now compare it with an already formatted data that we know is correct
        assert(exported_data == export.csv)

    def test_export_csv_div_format(self):
        """
        csv with div format test

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).format(EXPORT_FORMATS[1])
        # now compare it with an already formatted data that we know is correct
        assert(exported_data == export.csv_div)

    def test_export_excel_format(self):
        """
        excel format test

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).format(EXPORT_FORMATS[2])
        # now compare it with an already formatted data that we know is correct
        assert(len(exported_data) == 5632)

    def test_export_excel_div_format(self):
        """
        excel with div format test

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).format(EXPORT_FORMATS[3])
        # now compare it with an already formatted data that we know is correct
        assert(len(exported_data) == 5632)

    def test_export_text_format(self):
        """
        text format test

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).format(EXPORT_FORMATS[4])
        # now compare it with an already formatted data that we know is correct
        assert(exported_data == export.text)

    def test_export_browser_format(self):
        """
        browser format test

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).format(EXPORT_FORMATS[5])
        # now compare it with an already formatted data that we know is correct
        assert(exported_data == export.text)

    def test_export_csv_get(self):
        """
        test function `get` for csv format

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).get(EXPORT_FORMATS[0])
        # now check the status_code to be 200
        assert (exported_data.status_code == 200)

    def test_export_csv_div_get(self):
        """
        test function `get` for csv with div format

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).get(EXPORT_FORMATS[1])
        # now compare it with an already formatted data that we know is correct
        assert (exported_data.status_code == 200)

    def test_export_excel_get(self):
        """
        test function `get` for excel format

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).get(EXPORT_FORMATS[2])
        # now compare it with an already formatted data that we know is correct
        assert (exported_data.status_code == 200)

    def test_export_excel_div_get(self):
        """
        test function `get` for excel with div format

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).get(EXPORT_FORMATS[3])
        # now compare it with an already formatted data that we know is correct
        assert (exported_data.status_code == 200)

    def test_export_text_get(self):
        """
        test function `get` for text format

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).get(EXPORT_FORMATS[4])
        # now compare it with an already formatted data that we know is correct
        assert (exported_data.status_code == 200)

    def test_export_browser_get(self):
        """
        test function `get` for browser format

        """
        # format the stubdata using the code
        exported_data = Export(export.form_data).get(EXPORT_FORMATS[5])
        # now compare it with an already formatted data that we know is correct
        assert (exported_data.status_code == 200)

    def test_search_no_payload(self):
        """
        ensure that if no payload is passed in, returns 400

        """
        r = self.client.post('/search')
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "no information received"}')

    def test_export_no_payload(self):
        """
        ensure that if no payload is passed in, returns 400

        """
        r = self.client.post('/export')
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "no information received"}')

    def test_search_no_payload_param(self):
        """
        ensure that if payload without all the needed params is passed in, returns 400

        """
        r = self.client.post('/search', data=dict({'missingParamsPayload': ''}))
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "no bibcode found in payload (parameter name is `bibcode`)"}')

    def test_search_no_bibcode_payload(self):
        """
        ensure that if payload without all the needed params is passed in, returns 400

        """
        r = self.client.post('/search', data=dict({'bibcode': ''}))
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "no bibcode submitted"}')

    def test_export_no_payload_param(self):
        """
        ensure that if payload without all the needed params is passed in, returns 400

        """
        r = self.client.post('/export', data=dict({'missingParamsPayload': ''}))
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "no selection found in payload (parameter name is `selected`)"}')

    def test_payload_param_error_max_author(self):
        """
        ensure that if payload without all the needed params is passed in, returns 400

        """
        payload = {'bibcode': ["1994AAS...185.4102A","1994AAS...185.4104E"], 'maxauthor':-1}
        r = self.client.post('/search', data=dict(payload))
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "parameter maxauthor should be a positive integer >= 0"}')


    def test_payload_param_error_cutoff_year(self):
        """
        ensure that if payload without all the needed params is passed in, returns 400

        """
        payload = {'bibcode': ["1994AAS...185.4102A", "1994AAS...185.4104E"], 'numyears':-1}
        r = self.client.post('/search', data=dict(payload))
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "parameter numyears should be positive integer > 0"}')


    def test_payload_param_error_empty_selection(self):
        """
        ensure that if payload without all the needed params is passed in, returns 400

        """
        payload = {'selected': '', 'format':''}
        r = self.client.post('/export', data=dict(payload))
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "no selection submitted"}')


    def test_payload_param_error_wrong_format(self):
        """
        ensure that if payload without all the needed params is passed in, returns 400

        """
        payload = {'selected': ["Accomazzi, A.||2017/09"], 'format':''}
        r = self.client.post('/export', data=dict(payload))
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "unrecognizable export format specified"}')


    def test_payload_param_error_unrecognizable_format(self):
        """
        ensure that if payload without a correct format params is passed in, returns 400

        """
        payload = {'selected': ["Accomazzi, A.||2017/09"], 'format':'something wrong'}
        r = self.client.post('/export', data=dict(payload))
        status = r.status_code
        response = r.data
        self.assertEqual(status, 400)
        self.assertEqual(response, '{"error": "unrecognizable export format specified"}')

    def test_is_number(self):
        """
        ensure is_number behaves properly

        """
        self.assertEqual(is_number('1'), True)
        self.assertEqual(is_number('-1'), True)
        self.assertEqual(is_number('notnumber'), False)

    def test_xml_status(self):
        """
        ensure status is read properly

        """
        solr_data = \
            {
               "responseHeader":{
                  "status":0,
                  "QTime":1,
                  "params":{
                     "sort":"date desc",
                     "fq":"{!bitset}",
                     "rows":"19",
                     "q":"*:*",
                     "start":"0",
                     "wt":"json",
                     "fl":"author,aff_raw,pubdate"
                  }
               }
            }
        formatted_data = Formatter(solr_data)
        assert(formatted_data.get_status() == 0)

    def test_xml_no_num_docs(self):
        """
        ensure if no `response` found in json num_docs is set to 0

        """
        solr_data = \
            {
               "responseHeader":{
                  "status":1,
                  "QTime":1,
                  "params":{
                     "sort":"date desc",
                     "fq":"{!bitset}",
                     "rows":"19",
                     "q":"*:*",
                     "start":"0",
                     "wt":"json",
                     "fl":"author,aff_raw,pubdate"
                  }
               }
            }
        formatted_data = Formatter(solr_data)
        assert(formatted_data.get_num_docs() == 0)


    def test_is_complete(self):
        """
        ensure all necessary info was returned from solr

        """
        assert(Formatter(solrdata.data2).is_complete() == False)

if __name__ == '__main__':
  unittest.main()