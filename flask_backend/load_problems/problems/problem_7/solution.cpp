#include <iostream>
#include <string>
using namespace std;

string solve_logic(const string& s) {
    if(s.size() <= 10) return s;
    return s.front() + to_string(s.size() - 2) + s.back();
}

int main() {
    int n;
    cin >> n;
    for(int i = 0; i < n; i++) {
        string s;
        cin >> s;
        if(i > 0) cout << "\n";
        cout << solve_logic(s);
    }
    return 0;
}
