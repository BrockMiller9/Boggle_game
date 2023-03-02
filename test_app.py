from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with self.client:
            res = self.client.get('/board')
            html = res.get_data(as_text=True)
            self.assertIn("High Score: 0", html)

            print(res.data)
            self.assertIn('Score: 0', html)

    def test_check_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["R", "O", "K", "R", "T"],
                                 ["C", "C", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=rock')
        self.assertEqual(response.json['response'], 'ok')

    def test_not_on_board(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["R", "O", "K", "R", "T"],
                                 ["C", "C", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=board')
        self.assertEqual(response.json['response'], 'not-on-board')

    def test_not_a_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["R", "O", "K", "R", "T"],
                                 ["C", "C", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"],
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=brd')
        self.assertEqual(response.json['response'], 'not-word')
