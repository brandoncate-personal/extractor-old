import unittest
from unittest.mock import patch
from handlers import extractor, mocks

import json


class TestStringMethods(unittest.TestCase):

    @patch('flask.jsonify')
    def test_success__no_warning(self, mock_jsonify):
        # setup
        mock_request = mocks.Request({
            'repo': 'https://github.com/brandoncate-personal/blog-content'
        })
        mock_response = mocks.Response()
        mock_jsonify.return_value = mock_response
        # test
        resp = extractor.extract(mock_request)

        # assert
        self.assertEqual(resp, mock_response)
        self.assertEqual(resp.status_code, 200)

    @patch('flask.jsonify')
    def test_error_not_found(self, mock_jsonify):
        # setup
        mock_request = mocks.Request({
            'repo': 'https://github.com/BrandonCate95/appsync-react-posts-starter'
        })
        mock_response = mocks.Response()
        mock_jsonify.return_value = mock_response
        # test
        resp = extractor.extract(mock_request)

        print(resp)
        # assert
        self.assertEqual(resp, mock_response)
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
