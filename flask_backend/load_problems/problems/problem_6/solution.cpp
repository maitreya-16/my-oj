#include <iostream>
#include <string>
using namespace std;

string solve_logic(const string& s) {
    string result;
    size_t i = 0;
    while(i < s.size()) {
        size_t j = i;
        while(j < s.size() && s[j] == s[i]) j++;
        result += to_string(j - i);
        result += s[i];
        i = j;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    cout << solve_logic(s);
    return 0;
}
