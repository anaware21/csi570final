#!/bin/bash

# Directory containing the test cases
TEST_DIR="../CSCI570_Project/SampleTestCases"

# Python program to test
PROGRAM="python3 basic.py"

echo "===== Running Test Cases ====="

# Loop through input files
for input in $TEST_DIR/input*.txt; do
    # Extract the number (e.g., input3 → 3)
    base=$(basename "$input")
    num=${base//input/}
    num=${num//.txt/}

    expected="$TEST_DIR/output${num}.txt"
    actual="$TEST_DIR/my_output${num}.txt"

    echo -n "Test $num: "

    #  Run program
    $PROGRAM "$input" "$actual"

    trimmed_expected="$TEST_DIR/expected_trimmed_${num}.txt"
    trimmed_actual="$TEST_DIR/actual_trimmed_${num}.txt"

    # macOS-compatible delete last 2 lines
    sed '$d' "$expected" | sed '$d' > "$trimmed_expected"
    sed '$d' "$actual" | sed '$d' > "$trimmed_actual"

    # Compare
    if diff -q "$trimmed_expected" "$trimmed_actual" > /dev/null; then
        echo "PASS"
    else
        echo "FAIL ❌"
        echo "  Differences:"
        diff "$trimmed_expected" "$trimmed_actual"
    fi

    rm "$trimmed_expected" "$trimmed_actual"
done

echo "===== Done ====="