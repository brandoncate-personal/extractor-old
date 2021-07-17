import unittest
from unittest.mock import patch
from handlers import extractor, mocks


class TestStringMethods(unittest.TestCase):

    @patch('flask.jsonify')
    def test_upper(self, mock_jsonify):
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

if __name__ == '__main__':
    unittest.main()
