"""
Hirschberg Algorithm:
We generate forward cost and backward cost instead of building the full matrix.
That gives us the optimal split point in sequence Y / sequence 2.
Then we recursively solve the 2 subproblems.
"""

from utils import input_string_generator, alpha
import os
import sys
import time


# check if psutil installed for memory measurement
try:
    import psutil
    _HAS_PSUTIL = True
except:
    _HAS_PSUTIL = False
    import resource


delta = 30  # Gap penalty


# full dp for small base cases i.e len=1
def basic_dp(x, y):
    m, n = len(x), len(y)

    dp = [[0] * (n+1) for _ in range(m+1)]
    bt = [[-1] * (n+1) for _ in range(m+1)]

    for i in range(m+1):
        dp[i][0] = i*delta
        if i>0:
            bt[i][0] = 1

    for j in range(n+1):
        dp[0][j] = j*delta
        if j>0:
            bt[0][j] = 2

    for i in range(1, m+1):
        for j in range(1, n+1):
            diag = dp[i-1][j-1] + alpha(x[i-1], y[j-1])
            up = dp[i-1][j] + delta
            left = dp[i][j-1] + delta

            best = diag
            bt_dir = 0
            if up<best: 
                best = up
                bt_dir = 1
            if left<best:
                best = left
                bt_dir = 2

            dp[i][j] = best
            bt[i][j] = bt_dir

    # backtrack
    aligned_x = []
    aligned_y = []
    i, j = m, n

    while i>0 or j>0:
        if i>0 and j>0 and bt[i][j]==0:
            aligned_x.append(x[i-1])
            aligned_y.append(y[j-1])
            i-=1
            j-=1
        elif i>0 and (j==0 or bt[i][j]==1):
            aligned_x.append(x[i-1])
            aligned_y.append('_')
            i-=1
        else:
            aligned_x.append("_")
            aligned_y.append(y[j-1])
            j-=1

    aligned_x.reverse()
    aligned_y.reverse()

    aligned_x = ''.join(aligned_x)
    aligned_y = ''.join(aligned_y)
    
    return (int(dp[m][n]), aligned_x, aligned_y)


# computes only last row of table of dp table
# returns list of length n+1 containing dp costs
def dp_last_row(x, y):
    m = len(x)
    n = len(y)
    
    prev = [j*delta for j in range(n+1)]

    for i in range(1, m+1):
        curr = [0]*(n+1)
        curr[0] = i*delta

        for j in range(1, n+1):
            diag = prev[j-1] + alpha(x[i-1], y[j-1])
            up   = prev[j]   + delta
            left = curr[j-1] + delta

            best = diag
            if up < best:
                best = up
            if left < best:
                best = left
            curr[j] = best
        
        prev = curr
    
    return prev


def dp_last_row_reverse(x, y):
    # reverse both strings and compute last row, then reverse the row
    # so that R[j] corresponds to cost of aligning first part of x with second part of y
    last_rev = dp_last_row(x[::-1], y[::-1])

    return last_rev[::-1]


def hirschberg(x, y):
    m, n = len(x), len(y)

    # BASE CASES
    # BASE CASES
    #return int(dp[m][n], aligned_x, aligned_y)
    # for sequence length 0 and 1

    # RECURSION
    # splitting into left anf right halves
    # computing forward and backward dp, and the best split

    # should return cost, aligned_x, aligned_y

    # temporary: for now this function just calls basic_dp helper function
    
    # return basic_dp(x, y)
    
    if m == 0:
        # align empty x with y: all gaps in x
        aligned_x = "_" * n
        aligned_y = y
        return (n * delta, aligned_x, aligned_y)
    
    if n == 0:
        # align x with empty y: all gaps in y
        aligned_x = x
        aligned_y = "_" * m
        return (m * delta, aligned_x, aligned_y)
    
    if m == 1 or n == 1:
        # use basic DP for small cases
        return basic_dp(x, y)

    # RECURSION: split x in half
    mid = m // 2
    
    # Compute forward DP for first half of x
    x_first = x[:mid]
    forward = dp_last_row(x_first, y)
    
    # Compute backward DP for second half of x
    x_second = x[mid:]
    backward = dp_last_row_reverse(x_second, y)
    
    # Find optimal split point in y
    # We want to minimize forward[j] + backward[j] for j in [0, n]
    min_cost = float('inf')
    best_j = 0
    for j in range(n + 1):
        cost = forward[j] + backward[j]
        if cost < min_cost:
            min_cost = cost
            best_j = j
    
    # Recursively solve two subproblems
    y_left = y[:best_j]
    y_right = y[best_j:]
    
    cost_left, aligned_x_left, aligned_y_left = hirschberg(x_first, y_left)
    cost_right, aligned_x_right, aligned_y_right = hirschberg(x_second, y_right)
    
    # Combine results
    aligned_x = aligned_x_left + aligned_x_right
    aligned_y = aligned_y_left + aligned_y_right
    total_cost = cost_left + cost_right
    
    return (total_cost, aligned_x, aligned_y)



# main() is copy-pasted from basic.py
# NEEDS TO BE MODIFIED
def main():
    
    if len(sys.argv) != 3:
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        # generate
        seq1, seq2 = input_string_generator(input_file)

        # measure time and memory

        # before
        if _HAS_PSUTIL:
            m0 = psutil.Process(os.getpid()).memory_info().rss / 1024.0
        else:
            m0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        t0 = time.time()

        cost, aligned_seq1, aligned_seq2 = hirschberg(seq1, seq2)

        # after
        if _HAS_PSUTIL:
            m1 = psutil.Process(os.getpid()).memory_info().rss / 1024.0
        else:
            m1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        t1 = time.time()

        elapsed_time = (t1 - t0) * 1000.0
        mem_used = max(0.0, m1 - m0)

        # output
        with open(output_file, "w") as f:
            f.write(str(int(cost)) + "\n")
            f.write(aligned_seq1 + "\n")
            f.write(aligned_seq2 + "\n")
            f.write(str(elapsed_time) + "\n")
            f.write(str(mem_used))
        
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()