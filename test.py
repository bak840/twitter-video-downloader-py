import unittest

from main import get_id


class TestApp(unittest.TestCase):
    def test_get_id(self):
        url = 'https://twitter.com/bak840/status/1362860958092316675?s=20'
        result = get_id(url)
        self.assertEqual(result, '1362860958092316675')


if __name__ == '__main__':
    unittest.main()
