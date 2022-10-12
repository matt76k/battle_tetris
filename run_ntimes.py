import subprocess
import time
import os
import signal

scmd = "python3 ai_mode.py --nodisplay"
ccmd = "python3 client.py --timeout 120"

server = subprocess.Popen(scmd.split())

if __name__ == "__main__":
    try:
        score = []
        for i in range(10):
            time.sleep(0.1)
            res = subprocess.run(ccmd.split(), stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').split()[2]
            score.append(int(res))

        print(sum(score) / 10.0)
    finally:
        server.terminate()