#include <iostream>
#include <vector>
using namespace std;

int solve_logic(const vector<long long>& a) {
    int best = 1;
    int cur = 1;
    for(size_t i = 1; i < a.size(); i++) {
        if(a[i] > a[i - 1]) cur++;
        else cur = 1;
        if(cur > best) best = cur;
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> a(n);
    for(int i = 0; i < n; i++) cin >> a[i];
    cout << solve_logic(a);
    return 0;
}
