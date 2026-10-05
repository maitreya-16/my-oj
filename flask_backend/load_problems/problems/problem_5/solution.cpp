#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    long long left = 0;     // A[i-1]
    long long middle = 0;   // A[i]
    long long right;        // A[i+1]
    long long cnt = 0;

    for(int i = 0; i < n; i++) {
        cin >> right;
        // the middle value is counted only when it has a neighbour on both sides
        // and is strictly greater than each of them
        if(i >= 2 && middle > left && middle > right) cnt++;
        left = middle;
        middle = right;
    }

    cout << cnt;
    return 0;
}
