import glob
import os
import subprocess

for i in glob.glob('players/*'):
    if not os.path.exists(f"{i}/Player.py"):
        continue
        
    res = subprocess.run(f"python3 run_ntimes.py --player {i.replace('/', '.')}".split(), stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').rstrip('\r\n')
    print(f"{i.split('/')[1]}, {res}")