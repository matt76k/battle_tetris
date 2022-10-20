import subprocess
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--player1', type=str, default="Bot")
parser.add_argument('--player2', type=str, default="Bot")
parser.add_argument('--ntimes', type=int, default=3)
parser.add_argument('--timeout', type=int, default=10)

args = parser.parse_args()

scmd = f"python3 battle.py --nodisplay --timeout {args.timeout}"
p1cmd = f"python3 client.py --player {args.player1} --devnull"
p2cmd = f"python3 client.py --player {args.player2} --devnull"

if __name__ == "__main__":
    try:
        score = []
        for i in range(args.ntimes):
            time.sleep(0.2)
            server = subprocess.Popen(scmd.split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            subprocess.Popen(p1cmd.split(), stdout=subprocess.DEVNULL)
            subprocess.Popen(p2cmd.split(), stdout=subprocess.DEVNULL)
            server.wait()
            print(server.stdout.read().decode('utf-8').strip())

    except Exception as e:
        print(e)
