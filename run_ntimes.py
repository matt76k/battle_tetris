import subprocess
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--player', type=str, default="Bot")
parser.add_argument('--ntimes', type=int, default=3)
parser.add_argument('--timeout', type=int, default=10)

args = parser.parse_args()

scmd = "python3 ai_mode.py --nodisplay"
ccmd = f"python3 client.py --timeout {args.timeout} --player {args.player} --devnull"

server = subprocess.Popen(scmd.split())

if __name__ == "__main__":
    try:
        score = []
        for i in range(args.ntimes):
            time.sleep(0.2)
            res = subprocess.run(ccmd.split(), stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').split()[2]
            score.append(int(res))

        print(sum(score) / float(args.ntimes))
    finally:
        server.terminate()