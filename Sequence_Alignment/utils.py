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

# Add a main function to test the utility
if __name__ == "__main__":
    # Replace this path with the path to your input file
    input_file = "CSCI570_Project/SampleTestCases/input1.txt"  # relative path
    s, t = input_string_generator(input_file)