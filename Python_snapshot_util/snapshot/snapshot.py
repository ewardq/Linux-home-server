"""
Make snapshot

{"Tasks": {"total": 440, "running": 1, "sleeping": 354, "stopped": 1, "zombie": 0},
"%CPU": {"user": 14.4, "system": 2.2, "idle": 82.7},
"KiB Mem": {"total": 16280636, "free": 335140, "used": 11621308},
"KiB Swap": {"total": 16280636, "free": 335140, "used": 11621308},
"Timestamp": 1624400255}
"""
import argparse
import json
import os
import psutil
import time
import sys

class SystemMonitor:
    def __init__(self, interval=30, filename="snapshot.json", count=20):
        self.interval = interval
        self.filename = filename
        self.count = count

    def get_snapshot(self):
        try:
            # Count processes by status
            statuses = {'total': 0, 'running': 0, 'sleeping': 0, 'stopped': 0, 'zombie': 0}
            for proc in psutil.process_iter(attrs=['status']):
                statuses['total'] += 1
                status = proc.info['status']
                if status in statuses:
                    statuses[status] += 1

            # CPU usage
            cpu_times = psutil.cpu_times_percent(interval=0)
            cpu_info = {
                'user': cpu_times.user,
                'system': cpu_times.system,
                'idle': cpu_times.idle
            }

            # Memory
            mem = psutil.virtual_memory()
            mem_info = {
                'total': mem.total // 1024,
                'free': mem.free // 1024,
                'used': mem.used // 1024
            }

            # Swap
            swap = psutil.swap_memory()
            swap_info = {
                'total': swap.total // 1024,
                'free': swap.free // 1024,
                'used': swap.used // 1024
            }

            # Final snapshot
            snapshot = {
                'Tasks': statuses,
                '%CPU': cpu_info,
                'KiB Mem': mem_info,
                'KiB Swap': swap_info,
                'Timestamp': int(time.time())
            }
            return snapshot
        
        except Exception as e:
            return {"error": f"Failed to collect snapshot: {e}", "Timestamp": int(time.time())}

    def run(self):
        try:
            # Clear file at start
            open(self.filename, "w").close()
        except Exception as e:
            print(f"Error initializing output file: {e}", file=sys.stderr)
            return

        for i in range(self.count):
            snapshot = self.get_snapshot()
            try:
                with open(self.filename, "a") as f:
                    json.dump(snapshot, f)
                    f.write("\n")
            except Exception as e:
                print(f"Error writing to file: {e}", file=sys.stderr)

            try:
                os.system('clear')
                print(snapshot, end="\r")
            except Exception as e:
                print(f"Error printing snapshot: {e}", file=sys.stderr)

            try:
                time.sleep(self.interval)
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user.")
                break
            except Exception as e:
                print(f"Error during sleep: {e}", file=sys.stderr)    
            
def main():
    parser = argparse.ArgumentParser(description="Simple System Monitor")
    parser.add_argument("-i", help="Interval between snapshots in seconds", type=int, default=30)
    parser.add_argument("-f", help="Output file name", default="snapshot.json")
    parser.add_argument("-n", help="Quantity of snapshots to output", type=int, default=20)

    args = parser.parse_args()

    try:
        monitor = SystemMonitor(interval=args.i, filename=args.f, count=args.n)
        monitor.run()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()