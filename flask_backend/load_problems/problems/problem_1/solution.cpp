#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    long long value;
    cin >> value;
    long long smallest = value;
    long long largest = value;

    for(int i = 1; i < n; i++) {
        cin >> value;
        if(value < smallest) smallest = value;
        if(value > largest) largest = value;
    }

    cout << largest - smallest;
    return 0;
}
