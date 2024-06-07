import subprocess
import time

start_time = time.time()

# Command 1
command1 = [
    "python", "demos/demo_reconstruct.py",
    "-i", "TestSamples/examples",
    "--saveObj", "True",
    "--useTex", "True"
]

# Command 2: Shell Script
shell_script_command2 = ["./activate_env_and_run2.sh"]

# Command 3: Shell Script
shell_script_command3 = ["./activate_env_and_run3.sh"]

# Execute Command 1
print("Executing img to head recon...")
proc1 = subprocess.Popen(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout1, stderr1 = proc1.communicate()
if proc1.returncode != 0:
    print("Error executing head recon Command:")
    print(stderr1.decode())
    exit(1)
else:
    print("Head recon Command executed successfully.")

# Calculate time elapsed after Command 1
command1_time = time.time() - start_time

# Execute Command 2 (Shell Script)
print("\nExecuting shell script to activate Conda environment and run obj to fbx...")
proc2 = subprocess.Popen(shell_script_command2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout2, stderr2 = proc2.communicate()
if proc2.returncode != 0:
    print("Error executing shell script:")
    print(stderr2.decode())
    exit(1)
else:
    print("obj to fbx executed successfully.")

# Calculate time elapsed after Command 2
command2_time = time.time() - start_time - command1_time

# Execute Command 3 (Shell Script)
print("\nExecuting shell script to activate Conda environment and run merge head and body...")
proc3 = subprocess.Popen(shell_script_command3, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout3, stderr3 = proc3.communicate()
if proc3.returncode != 0:
    print("Error executing shell script 3:")
    print(stderr3.decode())
    exit(1)
else:
    print("Merge script executed successfully.")

# Calculate time elapsed after Command 3
command3_time = time.time() - start_time - command1_time - command2_time

# Total process time
total_time = time.time() - start_time

print("\nTotal Process Time:")
print("Command 1:", command1_time, "seconds")
print("Command 2:", command2_time, "seconds")
print("Command 3:", command3_time, "seconds")
print("Total Time:", total_time, "seconds")
