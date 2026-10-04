#include <iostream>
#include <vector>
using namespace std;

int solve_logic(int n) {
    // count primes strictly smaller than n
    if(n <= 2) return 0;
    vector<bool> composite(n, false);
    int count = 0;
    for(int i = 2; i < n; i++) {
        if(!composite[i]) {
            count++;
            for(long long j = (long long)i * i; j < n; j += i) composite[(size_t)j] = true;
        }
    }
    return count;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    cout << solve_logic(n);
    return 0;
}
