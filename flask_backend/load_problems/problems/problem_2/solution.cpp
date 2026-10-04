#include <iostream>
#include <string>
using namespace std;

int solve_logic(const string& s) {
    int count = 0;
    for(char c : s) {
        if(c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') count++;
    }
    return count;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    cout << solve_logic(s);
    return 0;
}
