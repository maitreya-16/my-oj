import sys


def solve_logic(a):
    return max(a) - min(a)


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    sys.stdout.write(str(solve_logic(a)))


main()
