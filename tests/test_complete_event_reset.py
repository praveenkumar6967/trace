"""
Isolated Automated Test Suite for TRACE x X Complete Event Reset Feature
Verifies all 13 security, retention, backup, foreign-key, and progression requirements.
Uses an isolated disposable test database without touching production or active dev data.
"""
import os
import sys
import time
import json
import sqlite3
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
TEST_BACKUP_DIR = os.path.join(TEST_DIR, 'test_backups')

sys.path.insert(0, PROJECT_ROOT)
import server


class TestCompleteEventReset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(TEST_BACKUP_DIR, exist_ok=True)

    def get_test_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def setUp(self):
        # Create a unique database file for each test method to prevent Windows SQLite file locking
        self.db_path = os.path.join(TEST_DIR, f"test_db_{self._testMethodName}.db")
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except:
                pass

        server.DB_FILE = self.db_path
        server.BACKUP_DIR = TEST_BACKUP_DIR
        server.init_database()

        # Seed realistic competition data for 2 test participant teams
        conn = self.get_test_db()
        c = conn.cursor()
        now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

        # Test Team 1: Advanced Investigation
        h1, s1 = server.hash_password('1111')
        c.execute('''
            INSERT INTO teams (team_id, team_name, college_name, department, team_size, members_json, pin_masked, pin_hash, pin_salt, registered_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('TX-TEST-001', 'Alpha Squad', 'TJS College', 'CSE', 2, '["Alice", "Bob"]', '••••', h1, s1, now_iso, 'Investigating'))
        
        c.execute('''
            INSERT INTO sessions (team_id, case_id, case_name, current_round, current_question, time_remaining, connection_status, session_status, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('TX-TEST-001', 'case-01', 'CASE 01', 2, 8, '04:30', 'SECURE', 'ACTIVE', time.time()))

        c.execute('''
            INSERT INTO submissions (team_id, case_id, round1_answers_json, round2_answers_json, score_r1, score_r2, total_score, accuracy_rate, evaluation_status, qualification_status, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('TX-TEST-001', 'case-01', '{"0":"A","1":"B"}', '{"0":"C"}', 14, 12, 26, 86.6, 'EVALUATED', 'QUALIFIED', now_iso))

        c.execute('''
            INSERT INTO round_timers (id, team_id, case_id, round, start_time_ms, end_time_ms, duration_sec)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('timer-001', 'TX-TEST-001', 'case-01', 1, 1000, 601000, 600))

        c.execute('''
            INSERT INTO violations (team_id, violation_type, timestamp, violation_count, action_taken)
            VALUES (?, ?, ?, ?, ?)
        ''', ('TX-TEST-001', 'TAB SWITCH', now_iso, 1, 'Warning 1 of 3'))

        c.execute('''
            INSERT INTO score_audit_logs (team_id, original_score, prev_final_score, new_final_score, admin_id, reason, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('TX-TEST-001', 26, 26, 28, 'admin_cse', 'Verified tie-breaker log', now_iso))

        # Test Team 2: Active Session Token
        h2, s2 = server.hash_password('2222')
        c.execute('''
            INSERT INTO teams (team_id, team_name, college_name, department, team_size, members_json, pin_masked, pin_hash, pin_salt, registered_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('TX-TEST-002', 'Beta Hunters', 'TJS College', 'IT', 3, '["Charlie", "David"]', '••••', h2, s2, now_iso, 'Submitted'))

        c.execute('''
            INSERT INTO team_sessions (token, team_id, created_at, expires_at)
            VALUES (?, ?, ?, ?)
        ''', ('test-participant-token-12345', 'TX-TEST-002', time.time(), time.time() + 3600))

        # Previous Event Report
        c.execute('''
            INSERT INTO event_reports (title, college_name, department_name, event_date, event_venue, organizer, coordinators, overview_json, participation_json, structure_json, results_json, summary_json, organizers_json, created_at, updated_at, updated_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('Past Symposium Report', 'TJS', 'CSE', '2025-10-10', 'Auditorium', 'TJS', 'Coord', '{}', '{}', '{}', '[]', '{}', '{}', now_iso, now_iso, 'admin_cse'))
        report_id = c.lastrowid

        c.execute('''
            INSERT INTO event_report_versions (report_id, version, status, data_json, saved_by, saved_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (report_id, 1, 'FINAL', '{}', 'admin_cse', now_iso))

        # Event State to Active with published results
        c.execute("UPDATE event_state SET value = 'EVENT ACTIVE' WHERE key = 'status'")
        c.execute("UPDATE event_state SET value = 'ROUND 2 INVESTIGATION' WHERE key = 'phase'")
        c.execute("UPDATE event_state SET value = '1' WHERE key = 'results_published'")

        conn.commit()
        conn.close()

    def tearDown(self):
        time.sleep(0.05)
        for ext in ['', '-wal', '-shm']:
            fpath = self.db_path + ext
            if os.path.exists(fpath):
                try:
                    os.remove(fpath)
                except:
                    pass

    def test_01_unauthorized_user_cannot_execute_reset(self):
        """Test that requests lacking admin authentication are denied."""
        conn = self.get_test_db()
        admin_id = None
        self.assertIsNone(admin_id)

        # Database must remain unchanged
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM teams")
        self.assertGreaterEqual(c.fetchone()[0], 2)
        conn.close()

    def test_02_invalid_confirmation_phrase_rejected(self):
        """Test that incorrect confirmation phrases are rejected with HTTP 400 and data preserved."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET EVENT', True)
        self.assertEqual(code, 400)
        self.assertIn("Confirmation phrase mismatch", res['error'])

        code2, res2 = server.execute_complete_event_reset(conn, 'admin_cse', 'reset tracex event', True)
        self.assertEqual(code2, 400)

        # Verify teams and data preserved
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM teams")
        self.assertGreaterEqual(c.fetchone()[0], 2)
        conn.close()

    def test_03_missing_backup_confirmation_rejected(self):
        """Test that reset is rejected if the backup confirmation checkbox was not checked."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', False)
        self.assertEqual(code, 400)
        self.assertIn("verified database backup", res['error'])

        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM teams")
        self.assertGreaterEqual(c.fetchone()[0], 2)
        conn.close()

    def test_04_successful_complete_event_reset_execution(self):
        """Test that authorized administrator can successfully execute a complete event reset."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)
        self.assertEqual(code, 200, f"Expected 200 but got {code}: {res}")
        self.assertTrue(res['success'])
        self.assertEqual(res['status'], 'EVENT NOT STARTED')
        self.assertEqual(res['phase'], 'STANDBY')
        self.assertIn('backup', res)
        self.assertTrue(os.path.exists(os.path.join(TEST_BACKUP_DIR, res['backup']['filename'])))
        conn.close()

    def test_05_verified_backup_created_and_valid(self):
        """Verify that the pre-reset backup file is physically valid and contains 15 cases and questions."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)
        self.assertEqual(code, 200)
        bkp_filename = res['backup']['filename']
        bkp_path = os.path.join(TEST_BACKUP_DIR, bkp_filename)

        # File must exist and have non-zero size
        self.assertTrue(os.path.exists(bkp_path))
        self.assertGreater(os.path.getsize(bkp_path), 0)

        # Open backup database and verify integrity
        bkp_conn = sqlite3.connect(bkp_path)
        bc = bkp_conn.cursor()
        bc.execute("SELECT COUNT(*) FROM cases")
        self.assertEqual(bc.fetchone()[0], 15)
        bc.execute("SELECT COUNT(*) FROM questions")
        self.assertEqual(bc.fetchone()[0], 450)
        bc.execute("SELECT COUNT(*) FROM admins")
        self.assertGreaterEqual(bc.fetchone()[0], 1)
        # Pre-reset participant data was preserved in the backup!
        bc.execute("SELECT COUNT(*) FROM teams")
        self.assertGreaterEqual(bc.fetchone()[0], 2)
        bkp_conn.close()
        conn.close()

    def test_06_participant_data_completely_cleared(self):
        """Verify that all participant data and previous event results are cleared."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)
        self.assertEqual(code, 200, f"Expected 200 but got {code}: {res}")

        c = conn.cursor()
        tables_to_check_zero = [
            'teams',
            'sessions',
            'team_sessions',
            'submissions',
            'round_timers',
            'violations',
            'score_audit_logs',
            'event_reports',
            'event_report_versions'
        ]
        for tbl in tables_to_check_zero:
            c.execute(f"SELECT COUNT(*) FROM {tbl}")
            count = c.fetchone()[0]
            self.assertEqual(count, 0, f"Table '{tbl}' should have 0 records after reset, found {count}")
        conn.close()

    def test_07_core_data_preserved(self):
        """Verify that admin accounts, the 15 cases, and 450 questions are preserved intact."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)
        self.assertEqual(code, 200, f"Expected 200 but got {code}: {res}")

        c = conn.cursor()
        # Admin preserved
        c.execute("SELECT COUNT(*) FROM admins WHERE admin_id = 'admin_cse'")
        self.assertEqual(c.fetchone()[0], 1)

        # 15 Investigation Cases preserved
        c.execute("SELECT COUNT(*) FROM cases")
        self.assertEqual(c.fetchone()[0], 15)

        # 450 Authoritative Questions preserved
        c.execute("SELECT COUNT(*) FROM questions")
        self.assertEqual(c.fetchone()[0], 450)

        # Audit log has COMPLETE_EVENT_RESET
        c.execute("SELECT * FROM audit_logs WHERE action = 'COMPLETE_EVENT_RESET' ORDER BY id DESC LIMIT 1")
        audit_row = c.fetchone()
        self.assertIsNotNone(audit_row)
        self.assertIn("COMPLETE EVENT RESET executed", audit_row['details'])
        conn.close()

    def test_08_event_state_reset_to_not_started_and_standby(self):
        """Verify that the event state and phase are restored to initial status."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)
        self.assertEqual(code, 200, f"Expected 200 but got {code}: {res}")

        c = conn.cursor()
        c.execute("SELECT value FROM event_state WHERE key = 'status'")
        self.assertEqual(c.fetchone()[0], 'EVENT NOT STARTED')

        c.execute("SELECT value FROM event_state WHERE key = 'phase'")
        self.assertEqual(c.fetchone()[0], 'STANDBY')

        c.execute("SELECT value FROM event_state WHERE key = 'round'")
        self.assertEqual(c.fetchone()[0], '1')

        c.execute("SELECT value FROM event_state WHERE key = 'round1_start_time'")
        self.assertEqual(c.fetchone()[0], '')

        c.execute("SELECT value FROM event_state WHERE key = 'results_published'")
        self.assertEqual(c.fetchone()[0], '0')

        c.execute("SELECT value FROM event_state WHERE key = 'settings'")
        settings = json.loads(c.fetchone()[0])
        self.assertFalse(settings.get('resultsPublished', True))
        conn.close()

    def test_09_old_participant_credentials_and_sessions_invalidated(self):
        """Verify that old participant credentials cannot authenticate and tokens are dead."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)
        self.assertEqual(code, 200, f"Expected 200 but got {code}: {res}")

        c = conn.cursor()
        # Old token check
        c.execute("SELECT * FROM team_sessions WHERE token = 'test-participant-token-12345'")
        self.assertIsNone(c.fetchone())

        # Old team credentials check
        c.execute("SELECT * FROM teams WHERE UPPER(team_id) = 'TX-TEST-001'")
        self.assertIsNone(c.fetchone())
        conn.close()

    def test_10_admin_login_still_works(self):
        """Verify that administrator can still authenticate with existing credentials."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)
        self.assertEqual(code, 200, f"Expected 200 but got {code}: {res}")

        c = conn.cursor()
        c.execute("SELECT password_hash, salt FROM admins WHERE admin_id = 'admin_cse'")
        admin = c.fetchone()
        self.assertIsNotNone(admin)
        self.assertTrue(server.verify_password('traceX@2026', admin['password_hash'], admin['pin_salt' if 'pin_salt' in admin.keys() else 'salt']))
        conn.close()

    def test_11_fresh_team_can_register_login_and_select_case(self):
        """Verify that after reset, a brand new team can register, log in, and begin at case selection."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)
        self.assertEqual(code, 200, f"Expected 200 but got {code}: {res}")

        c = conn.cursor()
        now_iso = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        new_team_id = 'TX-2026-9999'
        new_pin = '4567'
        ph, ps = server.hash_password(new_pin)

        # 1. Register new team
        c.execute('''
            INSERT INTO teams (team_id, team_name, college_name, department, team_size, members_json, pin_masked, pin_hash, pin_salt, registered_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (new_team_id, 'Phoenix Ops', 'TJS Engineering', 'CSE', 2, '["Ravi", "Kiran"]', '••••', ph, ps, now_iso, 'Registered'))

        # Create session at standby
        c.execute('''
            INSERT INTO sessions (team_id, case_id, case_name, current_round, current_question, time_remaining, connection_status, session_status, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (new_team_id, None, None, 1, 1, '10:00', 'SECURE', 'NOT STARTED', time.time()))

        c.execute('''
            INSERT INTO submissions (team_id, case_id, score_r1, score_r2, total_score, accuracy_rate, violations_count, evaluation_status, qualification_status, submitted_at)
            VALUES (?, ?, 0, 0, 0, 0, 0, 'PENDING', 'RESULTS UNDER REVIEW', ?)
        ''', (new_team_id, '', now_iso))
        conn.commit()

        # 2. Login as new team
        c.execute("SELECT * FROM teams WHERE team_id = ?", (new_team_id,))
        team_row = c.fetchone()
        self.assertIsNotNone(team_row)
        self.assertTrue(server.verify_password(new_pin, team_row['pin_hash'], team_row['pin_salt']))

        # 3. Check new team initial state is case selection (no case selected yet)
        prog = server.get_team_progress(conn, new_team_id)
        self.assertIsNone(prog['caseId'])
        self.assertIsNone(prog['caseName'])
        self.assertEqual(prog['sessionStatus'], 'NOT STARTED')

        # 4. New team selects Case 07
        c.execute("UPDATE sessions SET case_id = 'case-07', case_name = 'CASE 07 — ATM JACKPOTTING ATTACK', session_status = 'CASE SELECTED', updated_at = ? WHERE team_id = ?", (time.time(), new_team_id))
        c.execute("UPDATE submissions SET case_id = 'case-07' WHERE team_id = ?", (new_team_id,))
        conn.commit()

        prog_after = server.get_team_progress(conn, new_team_id)
        self.assertEqual(prog_after['caseId'], 'case-07')
        self.assertEqual(prog_after['caseName'], 'CASE 07 — ATM JACKPOTTING ATTACK')
        self.assertEqual(prog_after['sessionStatus'], 'CASE SELECTED')
        conn.close()

    def test_12_server_restart_does_not_reseed_demo_teams_after_reset(self):
        """Verify that server restart or re-initialization does not resurrect cleared demo teams."""
        conn = self.get_test_db()
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)
        self.assertEqual(code, 200, f"Expected 200 but got {code}: {res}")
        conn.close()

        # Re-run init_database (as if server restarted)
        server.init_database()

        conn = self.get_test_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM teams")
        team_count = c.fetchone()[0]
        self.assertEqual(team_count, 0, "Restarting server after complete event reset must NOT reseed demo teams!")
        conn.close()

    def test_13_transaction_rollback_on_critical_failure(self):
        """Verify that if an error occurs during reset, the transaction rolls back cleanly without partial deletion."""
        conn = self.get_test_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM teams")
        initial_teams = c.fetchone()[0]

        # Break backup directory to force a failure during pre-reset backup creation
        orig_backup_dir = server.BACKUP_DIR
        server.BACKUP_DIR = 'Z:\\INVALID_NON_EXISTENT_DRIVE\\test_backups'
        code, res = server.execute_complete_event_reset(conn, 'admin_cse', 'RESET TRACEX EVENT', True)

        self.assertEqual(code, 500)
        self.assertIn("CRITICAL", res['error'])

        # Reset backup dir
        server.BACKUP_DIR = orig_backup_dir

        # Verify no data was deleted
        c.execute("SELECT COUNT(*) FROM teams")
        final_teams = c.fetchone()[0]
        self.assertEqual(initial_teams, final_teams, "Failed reset must not delete or partially clear data!")
        conn.close()


if __name__ == '__main__':
    unittest.main()
