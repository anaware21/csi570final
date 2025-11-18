# CSCI 570 – Sequence Alignment Project

This repository contains the implementation for the sequence alignment project assigned in CSCI 570 (Analysis of Algorithms).

## Installation
### Python Requirements

Python 3.8+
Optional but recommended: psutil

Install psutil:
```
pip install psutil
```


## How to Run
### 1. Running the Python program directly

Windows:
```
python basic.py input.txt output.txt
```

macOS/Linux:
```
python3 basic.py input.txt output.txt
```

### 2. Running using the shell script

macOS / Linux / Git Bash / WSL:
```
chmod +x basic.sh
```

```
./basic.sh input.txt output.txt
```


## Input Format
Input file contains:

1. Base string s0
2. One or more integers (indexes for expansion of s)
3. Base string t0
4. One or more integers (indexes for expansion of t)

Example:
```
ACGT
1
2
TAC
0
```
`utils.py` will expand these according to the rules described in the project PDF.


## Output Format
The output file will contain exactly five lines:
```
<optimal_cost>
<aligned_string_1>
<aligned_string_2>
<time_in_milliseconds>
<memory_in_kilobytes>
```