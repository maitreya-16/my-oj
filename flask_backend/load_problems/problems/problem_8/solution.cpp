#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

struct Edge {
    int u, v, w;
};

int solve_logic(int n, vector<Edge>& edges) {
    sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
        return a.w < b.w;
    });

    int m = edges.size();
    vector<int> best(n + 1, 0);   // longest valid route ending at each station
    vector<int> pending(m, 0);
    int ans = 0;

    int i = 0;
    while(i < m) {
        int j = i;
        while(j < m && edges[j].w == edges[i].w) j++;

        // links of equal strength must not extend each other
        for(int k = i; k < j; k++) pending[k] = best[edges[k].u] + 1;
        for(int k = i; k < j; k++) {
            if(pending[k] > best[edges[k].v]) best[edges[k].v] = pending[k];
            if(pending[k] > ans) ans = pending[k];
        }
        i = j;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<Edge> edges(m);
    for(int i = 0; i < m; i++) cin >> edges[i].u >> edges[i].v >> edges[i].w;
    cout << solve_logic(n, edges);
    return 0;
}
