import os
import sys
import time

def read_input_file(file_path):
    """
    Reads sequences from a text file and returns them as a tuple of strings.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        tuple: A tuple containing:
            - str: The first string (s).
            - str: The second string (t).
            - list: The first list of integers (list1).
            - list: The second list of integers (list2).
    """

    s = None
    t = None

    list1 = []
    list2 = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
            
                if not line:
                    continue

                try:
                    # Try to convert the line to an integer
                    number = int(line)
                    
                    # It's a number. We need to decide which array to add it to.
                    if t is None:
                        # If we haven't found the second string (t) yet,
                        # this number must belong to the first list (array1).
                        list1.append(number)
                    else:
                        # If we HAVE found the second string (t),
                        # this number must belong to the second list (array2).
                        list2.append(number)
                        
                except ValueError:
                    # It's a string. We need to decide which variable to put it in.
                    if s is None:
                        # If we haven't found the first string (s) yet, this is it.
                        s = line
                    else:
                        # If we HAVE found the first string (s), this must be the second one (t).
                        t = line

        return s, t, list1, list2

    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")

def input_string_generator(file_path):
    """
    Reads sequences from a text file and returns them as a tuple of strings.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        tuple: A tuple containing two sequences (seq1, seq2).
    """
    s, t, list1, list2 = read_input_file(file_path)

    for j in list1:
        temp = s[:j+1] + s + s[j+1:]
        s = temp
    for k in list2:
        temp = t[:k+1] + t + t[k+1:]
        t = temp

    return s, t

def alpha(c1, c2):
    """Returns the value for matching a character."""
    alpha_matrix = [[0, 110, 48, 94],
                    [110, 0, 118, 48],
                    [48, 118, 0, 110],
                    [94, 48, 110, 0]
                    ]
    
    char_to_index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    return alpha_matrix[char_to_index[c1]][char_to_index[c2]]





# check if psutil installed for memory measurement
try:
    import psutil
    _HAS_PSUTIL = True
except:
    _HAS_PSUTIL = False
    import resource


delta = 30  # Gap penalty

def align_sequences(seq1, seq2):
    # Example alignment logic (to be implemented)
    m, n = len(seq1), len(seq2)

    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # backtracking table (0 diag, 1 up, 2 left)
    bt = [[-1 for _ in range(n + 1)] for _ in range(m + 1)]

    # Base Cases
    for i in range(m + 1):
        dp[i][0] = i * delta
        if i>0:
            bt[i][0] = 1  # from up

    for j in range(n + 1):
        dp[0][j] = j * delta
        if j>0:
            bt[0][j] = 2  # from left

    for i in range(1, m + 1):
        for j in range(1, n + 1):
                
            diag = dp[i-1][j-1] + alpha(seq1[i-1], seq2[j-1])
            up = dp[i-1][j] + delta
            left = dp[i][j-1] + delta
                
            # deterministic tie-breaking: diag, up, left
            # to preserve directions

            best = diag
            bt_dir = 0
            if up < best:
                best = up
                bt_dir = 1
            if left < best:
                best = left
                bt_dir = 2

            dp[i][j] = best
            bt[i][j] = bt_dir

    # backtrack
    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = m, n

    while i>0 or j>0:
        if i>0 and j>0 and bt[i][j] == 0:
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            i -= 1
            j -= 1
        elif i>0 and (j==0 or bt[i][j]==1):
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = "_" + aligned_seq2
            i -= 1
        else:
            aligned_seq1 = "_" + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            j -= 1

    return dp[m][n], aligned_seq1, aligned_seq2


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

        cost, aligned_seq1, aligned_seq2 = align_sequences(seq1, seq2)

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