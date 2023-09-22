import unittest
from unittest.mock import patch, mock_open, Mock

import sys
sys.path.append('..')
from lib.insert_contributor_content import read_file, write_file, fetch_github_info, map_question_to_heading, fetch_all_stargazers, build_markdown_content

class TestFetchGitHubInfo(unittest.TestCase):

    @patch('requests.get')
    
    def test_successful_api_call(self, mock_get):
        # Mock a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "test_name",
            "avatar_url": "test_avatar_url"
        }
        mock_get.return_value = mock_response

        # Run the function and test its return value
        result = fetch_github_info('test_username')
        self.assertEqual(result['name'], 'test_name')
        self.assertEqual(result['avatar_url'], 'test_avatar_url')

    @patch('requests.get')
    def test_unsuccessful_api_call(self, mock_get):
        # Mock an unsuccessful response
        mock_response = Mock()
        mock_response.status_code = 404  # Not found status code
        mock_get.return_value = mock_response

        # Run the function and test its return value
        result = fetch_github_info('test_username')
        self.assertEqual(result['name'], 'test_username')
        self.assertEqual(result['avatar_url'], 'https://i.ibb.co/X231Rq8/octo-no-one.png')

# TODO: Write tests for the other functions in lib/insert_contributor_content.py

if __name__ == '__main__':
    unittest.main()
