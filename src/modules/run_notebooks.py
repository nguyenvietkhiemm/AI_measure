import os
import sys
import subprocess

def run_notebooks(notebooks_path):
    print("Notebooks are running...")

    # Chạy lệnh nbconvert
    try:
        process = subprocess.run(
            [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", 
             "--ExecutePreprocessor.timeout=-1", notebooks_path],
            check=True,
            timeout=240,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print(process.stdout.decode())
        print(process.stderr.decode())
        
        # In kết quả
        if process.returncode == 0:
            print("Notebooks have finished running")
        else:
            print("Error occurred while running notebooks:")
            print(process.stderr.decode())
    
    except subprocess.CalledProcessError as e:
        print("Error occurred while running nbconvert:")
        print(e.stderr.decode())

