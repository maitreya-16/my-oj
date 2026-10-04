#include <iostream>
#include <string>
using namespace std;

long long solve_logic(const string& s) {
    long long total = 0;
    for(unsigned char c : s) total += c;
    return total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    getline(cin, s);
    while(!s.empty() && (s.back() == '\r' || s.back() == '\n')) s.pop_back();
    cout << solve_logic(s);
    return 0;
}
