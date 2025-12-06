# collect_datapoints.py
import os
import subprocess
from utils import input_string_generator
import matplotlib.pyplot as plt
import csv

DATA_DIR = "../CSCI570_Project/Datapoints"
RESULT_DIR = "../CSCI570_Project/DatapointResults"
CSV_FILE = "../CSCI570_Project"
os.makedirs(RESULT_DIR, exist_ok=True)

basic_prog = ["python3", "basic.py"]
eff_prog   = ["python3", "efficient.py"]

rows = []
for fname in sorted(os.listdir(DATA_DIR)):
    if not fname.startswith("in") or not fname.endswith(".txt"):
        continue

    input_path = os.path.join(DATA_DIR, fname)

    # problem size m+n
    s1, s2 = input_string_generator(input_path)
    size = len(s1) + len(s2)

    num = fname.replace("input", "").replace(".txt", "")
    out_basic = os.path.join(RESULT_DIR, f"basic_{num}.txt")
    out_eff   = os.path.join(RESULT_DIR, f"efficient_{num}.txt")

    # run basic
    subprocess.run(basic_prog + [input_path, out_basic], check=True)
    # run efficient
    subprocess.run(eff_prog + [input_path, out_eff], check=True)

    # read last two lines: time, mem
    def read_time_mem(path):
        with open(path) as f:
            lines = [line.strip() for line in f.readlines() if line.strip() != ""]
        time_ms = float(lines[-2])
        mem_kb  = float(lines[-1])
        return time_ms, mem_kb

    t_b, m_b = read_time_mem(out_basic)
    t_e, m_e = read_time_mem(out_eff)

    rows.append((size, t_b, m_b, t_e, m_e))

rows.sort(key=lambda x: x[0])

with open(f"{CSV_FILE}/datapoints_stats.csv", "w") as f:
    f.write("size,time_basic,mem_basic,time_efficient,mem_efficient\n")
    for r in rows:
        f.write(",".join(str(x) for x in r) + "\n")

print("Written datapoints_stats.csv")


# Plotting
sizes = []
time_basic = []
time_eff = []
mem_basic = []
mem_eff = []

with open(f"{CSV_FILE}/datapoints_stats.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sizes.append(int(row["size"]))
        time_basic.append(float(row["time_basic"]))
        time_eff.append(float(row["time_efficient"]))
        mem_basic.append(float(row["mem_basic"]))
        mem_eff.append(float(row["mem_efficient"]))

# 1. CPU time vs problem size
plt.figure()
plt.plot(sizes, time_basic, marker="o", label="Basic")
plt.plot(sizes, time_eff, marker="o", label="Efficient")
plt.xlabel("Problem size (m + n)")
plt.ylabel("CPU time (ms)")
plt.title("CPU time vs Problem size")
plt.legend()
plt.grid(True)
plt.savefig(f"{CSV_FILE}/time_vs_size.png", dpi=200)

# 2. Memory vs problem size
plt.figure()
plt.plot(sizes, mem_basic, marker="o", label="Basic")
plt.plot(sizes, mem_eff, marker="o", label="Efficient")
plt.xlabel("Problem size (m + n)")
plt.ylabel("Memory usage (KB)")
plt.title("Memory usage vs Problem size")
plt.legend()
plt.grid(True)
plt.savefig(f"{CSV_FILE}/memory_vs_size.png", dpi=200)

