import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import builtins
import time
import sys
from snapshot.snapshot import SystemMonitor, main

class TestSystemMonitor(unittest.TestCase):

    @patch('psutil.process_iter')
    @patch('psutil.cpu_times_percent')
    @patch('psutil.virtual_memory')
    @patch('psutil.swap_memory')
    @patch('time.time', return_value=1624400255)
    def test_get_snapshot_success(self, mock_time, mock_swap, mock_mem, mock_cpu, mock_proc_iter):
        # Mock process statuses
        mock_proc_iter.return_value = [
            MagicMock(info={'status': 'running'}),
            MagicMock(info={'status': 'sleeping'}),
        ]

        # Mock CPU
        mock_cpu.return_value = MagicMock(user=10.0, system=5.0, idle=85.0)

        # Mock memory
        mock_mem.return_value = MagicMock(total=1024*1024, free=512*1024, used=512*1024)
        mock_swap.return_value = MagicMock(total=2048*1024, free=1024*1024, used=1024*1024)

        sm = SystemMonitor()
        snapshot = sm.get_snapshot()

        # Check structure
        self.assertIn('Tasks', snapshot)
        self.assertIn('%CPU', snapshot)
        self.assertIn('KiB Mem', snapshot)
        self.assertIn('KiB Swap', snapshot)
        self.assertIn('Timestamp', snapshot)

        self.assertEqual(snapshot['Tasks']['total'], 2)
        self.assertEqual(snapshot['%CPU']['user'], 10.0)
        self.assertEqual(snapshot['KiB Mem']['total'], 1024)

    @patch('psutil.process_iter', side_effect=Exception('psutil error'))
    @patch('time.time', return_value=1624400255)
    def test_get_snapshot_failure(self, mock_time, mock_proc_iter):
        sm = SystemMonitor()
        snapshot = sm.get_snapshot()
        self.assertIn('error', snapshot)
        self.assertIn('Timestamp', snapshot)
        self.assertTrue(snapshot['error'].startswith('Failed to collect snapshot'))

    @patch('time.sleep', return_value=None)
    @patch('os.system', return_value=0)
    @patch('builtins.open', new_callable=mock_open)
    @patch.object(SystemMonitor, 'get_snapshot', return_value={'test': 'snapshot'})
    def test_run_writes_snapshots(self, mock_get_snapshot, mock_open_file, mock_os_system, mock_sleep):
        sm = SystemMonitor(interval=1, count=3, filename='test.json')
        sm.run()

        # File should be opened at least 4 times (1 for clear + 3 writes)
        self.assertGreaterEqual(mock_open_file.call_count, 4)
        # get_snapshot called for each iteration
        self.assertEqual(mock_get_snapshot.call_count, 3)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=type('obj', (object,), {'i': 1, 'f': 'out.json', 'n': 2}))
    @patch.object(SystemMonitor, 'run')
    def test_main_invokes_system_monitor(self, mock_run, mock_parse_args):
        main()
        self.assertTrue(mock_run.called)

    @patch('builtins.open', side_effect=Exception('file error'))
    def test_run_file_init_failure(self, mock_open_file):
        sm = SystemMonitor()
        # Should catch the exception and return early without raising
        sm.run()  # No exception should be raised

    @patch('time.sleep', side_effect=KeyboardInterrupt)
    @patch('builtins.open', new_callable=mock_open)
    @patch.object(SystemMonitor, 'get_snapshot', return_value={'test': 'snapshot'})
    def test_run_keyboard_interrupt(self, mock_get_snapshot, mock_open_file, mock_sleep):
        sm = SystemMonitor(interval=1, count=5)
        # Should gracefully exit on keyboard interrupt
        sm.run()
        self.assertTrue(mock_get_snapshot.called)


if __name__ == '__main__':      # pragma: no cover
    unittest.main()