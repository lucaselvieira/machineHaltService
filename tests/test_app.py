import unittest
from app import app, machine_halts


class MachineHaltTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.app.post('/machine-halt', json={
            "machine_tag": "machine_1",
            "start_time": "2024-07-31T21:30:00.000Z"
        })

    def tearDown(self):
        response = self.app.delete('/machine-halt/all')
        print("Teardown response:", response.status_code, "\n")

    def test_a_create_halt(self):
        response = self.app.post('/machine-halt', json={
            "machine_tag": "machine_2",
            "start_time": "2024-07-31T22:30:00.000Z"
        })
        print("Create response= ", response.json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['machine_tag'], "machine_2")

    def test_b_get_halt(self):
        self.app.post('/machine-halt', json={
            "machine_tag": "machine_2",
            "start_time": "2024-07-31T22:30:00.000Z"
        })
        response = self.app.post('/machine-halt', json={
            "machine_tag": "machine_3",
            "start_time": "2024-07-31T23:30:00.000Z"
        })
        halt_id = response.json['id']
        response = self.app.get(f'/machine-halt/{halt_id}')
        print("Get response= ", response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], halt_id)

    def test_c_list_halts(self):
        response = self.app.get('/machine-halt/list', query_string={
            "machine_tag": "machine_1",
            "interval_start": "2024-07-31T21:00:00.000Z",
            "interval_end": "2024-07-31T22:00:00.000Z"
        })
        print("List response= ", response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_d_update_halt(self):
        response = self.app.post('/machine-halt', json={
            "machine_tag": "machine_2",
            "start_time": "2024-07-31T22:30:00.000Z"
        })
        halt_id = response.json['id']
        response = self.app.put('/machine-halt', json={
            "id": halt_id,
            "end_time": "2024-07-31T23:30:00.000Z"
        })
        print("Update end_time response= ", response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['end_time'], "2024-07-31T23:30:00.000Z")

    def test_e_update_halt(self):
        response = self.app.post('/machine-halt', json={
            "machine_tag": "machine_2",
            "start_time": "2024-07-31T22:30:00.000Z"
        })
        halt_id = response.json['id']
        response = self.app.put('/machine-halt', json={
            "id": halt_id,
            "reason": "scheduled"
        })
        print("Update reason response= ", response.get_json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['reason'], "scheduled")

    def test_f_delete_all_halts(self):
        # Create halts to delete
        self.app.post('/machine-halt', json={
            "machine_tag": "machine_2",
            "start_time": "2024-07-31T20:10:00.000Z"
        })
        self.app.post('/machine-halt', json={
            "machine_tag": "machine_3",
            "start_time": "2024-07-31T20:15:00.000Z"
        })
        self.assertEqual(len(machine_halts), 3)  # Verify there are 2 halts
        print("Delete response machine_halts before delete= ", machine_halts)

        response = self.app.delete('/machine-halt/all')
        print("Delete response= ", response.status_code)
        self.assertEqual(response.status_code, 204)
        print("Delete response machine_halts after delete= ", machine_halts)
        self.assertEqual(len(machine_halts), 0)


if __name__ == '__main__':
    unittest.main()
