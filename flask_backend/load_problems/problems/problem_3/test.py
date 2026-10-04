import random
import os
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def count_primes_below(n):
    # Sieve of Eratosthenes, counts primes p with p < n
    if n <= 2:
        return 0
    sieve = bytearray([1]) * n
    sieve[0] = 0
    sieve[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(range(i * i, n, i)))
    return sum(sieve)

testcases = []

# Minimum and tiny cases
testcases.append(2)                                      # minimum N, no primes below it
testcases.append(3)                                      # only 2 is below

# General cases
testcases.append(10)                                     # 2, 3, 5, 7
testcases.append(20)
testcases.append(25)                                     # N is not prime
testcases.append(50)

# N itself is prime vs. N just above a prime: N must NOT be counted
testcases.append(97)                                     # 97 is prime, strictly smaller means it is excluded
testcases.append(100)

# Large cases (near constraint)
testcases.append(999983)                                 # largest prime below 10^6, excluded
testcases.append(1000000)                                # maximum N

# Generate files
for i, n in enumerate(testcases, start=1):
    input_path = os.path.join(BASE_DIR, f"input{i}.txt")
    output_path = os.path.join(BASE_DIR, f"output{i}.txt")

    with open(input_path, "w", newline="\n") as f:
        f.write(str(n))

    with open(output_path, "w", newline="\n") as f:
        f.write(str(count_primes_below(n)))

# Verify solution.cpp against the generated files
def verify():
    source = os.path.join(BASE_DIR, "solution.cpp")
    compiler = shutil.which("g++")
    if compiler is None:
        print("g++ not found: test files generated, solution.cpp check skipped")
        return 0
    if not os.path.exists(source):
        print("solution.cpp not found")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        exe = os.path.join(tmp, "solution.exe" if os.name == "nt" else "solution")
        build = subprocess.run([compiler, "-O2", "-std=c++17", "-o", exe, source],
                               capture_output=True, text=True)
        if build.returncode != 0:
            print("Compilation failed")
            print(build.stderr)
            return 1

        passed = 0
        total = len(testcases)
        for i in range(1, total + 1):
            with open(os.path.join(BASE_DIR, f"input{i}.txt")) as f:
                data = f.read()
            with open(os.path.join(BASE_DIR, f"output{i}.txt")) as f:
                expected = f.read()
            try:
                run = subprocess.run([exe], input=data, capture_output=True, text=True, timeout=10)
                ok = run.returncode == 0 and run.stdout.split() == expected.split()
            except subprocess.TimeoutExpired:
                ok = False
            if ok:
                passed += 1
            print(f"Test {i}: {'PASSED' if ok else 'FAILED'}")

    print(f"{passed}/{total} test cases passed")
    return 0 if passed == total else 1

sys.exit(verify())
