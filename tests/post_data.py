import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        import requests

        data = {

        }
        url = "http://localhost:8000/api/post_data"
        response = requests.post(url, json=data)
        print(response.text)
        self.assertEqual(response.text, "200")  # add assertion here


if __name__ == '__main__':
    unittest.main()
