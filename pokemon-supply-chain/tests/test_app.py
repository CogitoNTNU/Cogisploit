import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import app as challenge


class ChallengeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original_db = challenge.DB
        challenge.DB = Path(self.temp.name) / "test.sqlite3"
        self.client = challenge.app.test_client()
        self.editor = challenge.editor.test_client()
        self.env = patch.dict(os.environ, {"NTNU_API_KEY": "test-key", "FLAG": "cogito{test_only}"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        challenge.DB = self.original_db
        self.temp.cleanup()

    def model(self, team):
        return Mock(json=lambda: {"choices": [{"message": {"content": json.dumps({"team": team})}}]})

    def test_editor_changes_only_notes_and_escapes_html(self):
        self.assertEqual(self.editor.post('/edit/129', data={'entry': 'Edited entry', 'notes': '<script>bad()</script>', 'stats': 999}).status_code, 200)
        entry = next(p for p in challenge.entries() if p['id'] == 129)
        self.assertEqual((entry['name'], entry['stats']), ('Magikarp', 200))
        self.assertEqual(entry['entry'], 'Edited entry')
        self.assertIn(b'&lt;script&gt;bad()', self.client.get('/').data)
        self.assertEqual(self.editor.post('/edit/999', data={'notes': 'x'}).status_code, 404)
        self.assertEqual(self.editor.post('/edit/129', data={'notes': 'x' * 4001}).status_code, 400)
        self.editor.post('/reset')
        self.assertEqual(challenge.entries()[5]['entry'], challenge.SEED[5]['entry'])
        self.assertEqual(challenge.entries()[5]['notes'], '')

    def test_poison_reaches_model_but_flag_does_not(self):
        self.editor.post('/edit/129', data={'entry': 'Poisoned upstream entry', 'notes': 'Community notes'})
        with patch('app.requests.post', return_value=self.model([129] * 6)) as transport:
            result = self.client.post('/build').json
        self.assertTrue(result['won'])
        self.assertEqual(result['flag'], 'cogito{test_only}')
        messages = json.dumps(transport.call_args.kwargs['json']['messages'])
        self.assertIn('Poisoned upstream entry', messages)
        self.assertNotIn('cogito{test_only}', messages)
        self.assertNotIn('magikarp', challenge.SYSTEM.lower())
        self.assertNotIn('ctf', challenge.SYSTEM.lower())
        self.assertEqual(transport.call_args.args[0], 'https://llm.hpc.ntnu.no/v1/chat/completions')
        self.assertEqual(result['team'][0]['image'], '/static/pokemon/129.png')

    def test_ports_have_separate_routes(self):
        for path in ('/edit/129', '/reset'):
            self.assertEqual(self.client.post(path).status_code, 404)
        self.assertEqual(self.editor.post('/build').status_code, 404)
        self.assertNotIn(b'<textarea', self.client.get('/').data)
        self.assertIn(b'<textarea', self.editor.get('/').data)

    def test_cached_pokeapi_entries_and_artwork_exist(self):
        for p in challenge.SEED:
            self.assertTrue(p['source'].startswith('https://pokeapi.co/'))
            self.assertTrue(p['entry'])
            with self.client.get(f"/static/pokemon/{p['id']}.png") as response:
                self.assertEqual(response.status_code, 200)

    def test_clean_team_does_not_win(self):
        with patch('app.requests.post', return_value=self.model([6, 9, 65, 94, 143, 149])):
            result = self.client.post('/build').json
        self.assertFalse(result['won'])
        self.assertIsNone(result['flag'])

    def test_powerful_pokemon_are_available_and_selectable(self):
        expected = {150: 'Mewtwo', 248: 'Tyranitar', 376: 'Metagross', 384: 'Rayquaza', 445: 'Garchomp'}
        roster = {p['id']: p for p in challenge.entries()}
        for species, name in expected.items():
            self.assertEqual(roster[species]['name'], name)
            self.assertGreaterEqual(roster[species]['stats'], 600)
        with patch('app.requests.post', return_value=self.model([150, 248, 376, 384, 445, 149])):
            response = self.client.post('/build')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['team'][0]['name'], 'Mewtwo')

    def test_invalid_model_teams_are_rejected(self):
        for team in ([129] * 5, ['129'] * 6, [999] * 6, [True] * 6, None):
            with self.subTest(team=team), patch('app.requests.post', return_value=self.model(team)):
                self.assertEqual(self.client.post('/build').status_code, 502)

    def test_missing_key_is_explicit(self):
        with patch.dict(os.environ, {'NTNU_API_KEY': ''}), patch('app.requests.post') as transport:
            self.assertEqual(self.client.post('/build').status_code, 503)
            transport.assert_not_called()


if __name__ == '__main__':
    unittest.main()
