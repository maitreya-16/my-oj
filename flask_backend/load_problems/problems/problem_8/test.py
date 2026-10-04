import random
import os
import shutil
import subprocess
import sys
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def longest_route(n, edges):
    order = sorted(edges, key=lambda e: e[2])
    best = [0] * (n + 1)
    ans = 0
    i = 0
    m = len(order)
    while i < m:
        j = i
        while j < m and order[j][2] == order[i][2]:
            j += 1
        # links of equal strength must not extend each other
        pending = [best[order[k][0]] + 1 for k in range(i, j)]
        for k in range(i, j):
            v = order[k][1]
            if pending[k - i] > best[v]:
                best[v] = pending[k - i]
            if pending[k - i] > ans:
                ans = pending[k - i]
        i = j
    return ans

def random_small(n, m, max_w):
    pairs = [(u, v) for u in range(1, n + 1) for v in range(1, n + 1) if u != v]
    chosen = random.sample(pairs, m)
    return n, [(u, v, random.randint(1, max_w)) for u, v in chosen]

def layered(n, m, layers):
    # Layers of 2 stations; each station links to both stations of the next layer.
    # All links between two neighbouring layers share one strength, so the number of
    # valid routes doubles with every layer: trying every route one by one never finishes.
    # The rest of the network is filled with random links.
    perm = list(range(1, n + 1))
    random.shuffle(perm)
    used = set()
    edges = []
    for g in range(layers - 1):
        strength = 100000 if g == layers - 2 else 400 * (g + 1)
        for u in (perm[2 * g], perm[2 * g + 1]):
            for v in (perm[2 * g + 2], perm[2 * g + 3]):
                used.add((u, v))
                edges.append((u, v, strength))
    while len(edges) < m:
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u == v or (u, v) in used:
            continue
        used.add((u, v))
        edges.append((u, v, random.randint(1, 100000)))
    random.shuffle(edges)
    return n, edges

def dense(n, m, max_w):
    codes = random.sample(range(n * n), n * n)
    edges = []
    for code in codes:
        u = code // n + 1
        v = code % n + 1
        if u == v:
            continue
        edges.append((u, v, random.randint(1, max_w)))
        if len(edges) == m:
            break
    return n, edges

random.seed(20260103)

testcases = []

# Small cases
testcases.append((3, [(1, 2, 1), (2, 3, 1), (3, 1, 1)]))          # cycle, all strengths equal
testcases.append((3, [(1, 2, 1), (2, 3, 2), (3, 1, 3)]))          # cycle, rising strengths
testcases.append((6, [(1, 2, 1), (3, 2, 5), (2, 4, 2), (2, 5, 2),
                      (2, 6, 9), (5, 4, 3), (4, 3, 4)]))          # general case

# Minimum cases
testcases.append((2, [(1, 2, 5)]))                                # minimum N and M
testcases.append((2, [(1, 2, 1), (2, 1, 2)]))                     # two stations, links in both directions

# Equal strengths and repeated stations
testcases.append((6, [(4, 5, 2), (1, 2, 1), (5, 6, 3),
                      (3, 4, 2), (2, 3, 1)]))                     # path with repeated strengths
testcases.append((4, [(4, 1, 6), (1, 3, 3), (2, 1, 2),
                      (1, 4, 5), (3, 1, 4), (1, 2, 1)]))          # route returns to station 1 again and again
testcases.append(random_small(8, 20, 4))                          # small dense graph, many ties

# Large cases (near constraint)
testcases.append(layered(1000, 2000, 250))                        # maximum N, M and W, astronomically many routes
testcases.append(dense(46, 2000, 40))                             # maximum M, dense graph, heavy ties

# Generate files
for i, (n, edges) in enumerate(testcases, start=1):
    input_path = os.path.join(BASE_DIR, f"input{i}.txt")
    output_path = os.path.join(BASE_DIR, f"output{i}.txt")

    with open(input_path, "w", newline="\n") as f:
        lines = [f"{n} {len(edges)}"] + [f"{u} {v} {w}" for u, v, w in edges]
        f.write("\n".join(lines))

    with open(output_path, "w", newline="\n") as f:
        f.write(str(longest_route(n, edges)))

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
