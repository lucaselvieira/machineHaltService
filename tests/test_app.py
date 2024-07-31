import unittest

from app import create_app, db


class MachineHaltTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.client.post('/machine-halt', json={
                "machine_tag": "machine_1",
                "start_time": "2024-07-31T21:30:00.000Z"
            })

    def tearDown(self):
        with self.app.app_context():
            response = self.client.delete('/machine-halt/all')
            print("Teardown response:", response.status_code, "\n")
            db.drop_all()

    def test_a_create_halt(self):
        response = self.client.post('/machine-halt', json={
            "machine_tag": "machine_2",
            "start_time": "2024-07-31T22:30:00.000Z"
        })
        print("Create response= ", response.json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['machine_tag'], "machine_2")

    def test_b_get_halt(self):
        self.client.post('/machine-halt', json={
            "machine_tag": "machine_2",
            "start_time": "2024-07-31T22:30:00.000Z"
        })
        response = self.client.post('/machine-halt', json={
            "machine_tag": "machine_3",
            "start_time": "2024-07-31T23:30:00.000Z"
        })
        halt_id = response.json['id']
        response = self.client.get(f'/machine-halt/{halt_id}')
        print("Get response= ", response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], halt_id)

    def test_c_list_halts(self):
        response = self.client.get('/machine-halt/list', query_string={
            "machine_tag": "machine_1",
            "interval_start": "2024-07-31T21:00:00.000Z",
            "interval_end": "2024-07-31T22:00:00.000Z"
        })
        print("List response= ", response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_d_update_halt(self):
        response = self.client.post('/machine-halt', json={
            "machine_tag": "machine_2",
            "start_time": "2024-07-31T22:30:00.000Z"
        })
        halt_id = response.json['id']
        response = self.client.put('/machine-halt', json={
            "id": halt_id,
            "end_time": "2024-07-31T23:30:00.000Z"
        })
        print("Update end_time response= ", response.get_json())

    def test_e_update_halt(self):
        response = self.client.post('/machine-halt', json={
            "machine_tag": "machine_2",
            "start_time": "2024-07-31T22:30:00.000Z"
        })
        halt_id = response.json['id']
        response = self.client.put('/machine-halt', json={
            "id": halt_id,
            "reason": "scheduled"
        })
        print("Update reason response= ", response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['reason'], "scheduled")

if __name__ == '__main__':
    unittest.main()
