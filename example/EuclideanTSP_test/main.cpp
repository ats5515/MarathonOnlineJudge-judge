#include <assert.h>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <vector>
using namespace std;

const int64_t CYCLES_PER_SEC = 2400000000;
const double TIMELIMIT = 2.8;
struct Timer {
	int64_t start;
	Timer() { reset(); }
	void reset() { start = getCycle(); }
	void plus(double a) { start -= (a * CYCLES_PER_SEC); }
	inline double get() { return (double)(getCycle() - start) / CYCLES_PER_SEC; }
	inline int64_t getCycle() {
		uint32_t low, high;
		__asm__ volatile("rdtsc"
						 : "=a"(low), "=d"(high));
		return ((int64_t)low) | ((int64_t)high << 32);
	}
};
class XorShift {
   public:
	unsigned int x, y, z, w;
	double nL[65536];

	XorShift() {
		init();
	}

	void init() {
		x = 314159265;
		y = 358979323;
		z = 846264338;
		w = 327950288;
		double n = 1 / (double)(2 * 65536);
		for (int i = 0; i < 65536; i++) {
			nL[i] = log(((double)i / 65536) + n);
		}
	}

	inline unsigned int next() {
		unsigned int t = x ^ x << 11;
		x = y;
		y = z;
		z = w;
		return w = w ^ w >> 19 ^ t ^ t >> 8;
	}

	inline double nextLog() {
		return nL[next() & 0xFFFF];
	}

	inline int nextInt(int m) {
		return (int)(next() % m);
	}

	int nextInt(int min, int max) {
		return min + nextInt(max - min + 1);
	}

	inline double nextDouble() {
		return (double)next() / ((long long)1 << 32);
	}
};
struct TSP {
	Timer timer;
	XorShift rnd;
	int N;
	vector<int> X;
	vector<int> Y;
	vector<int> res;
	vector<vector<double> > distMap;
	double dst(int x1, int y1, int x2, int y2) {
		return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
	}
	void input() {
		cin >> N;
		cerr << "N=" << N << endl;
		X.resize(N);
		Y.resize(N);
		for (int i = 0; i < N; i++) {
			cin >> X[i] >> Y[i];
		}
	}
	void output() {
		for (int i = 0; i < N; i++) {
			cout << res[i] << endl;
		}
	}
	double calcScore(vector<int> &v) {
		double score = 0;
		for (int i = 0; i < N - 1; i++) {
			score += distMap[v[i]][v[i + 1]];
		}
		score += distMap[v[N - 1]][v[0]];
		return score;
	}
	void init() {
		res.resize(N);
		for (int i = 0; i < N; i++) {
			res[i] = i;
		}
		distMap.resize(N, vector<double>(N, 0));
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < i; j++) {
				double d = dst(X[i], Y[i], X[j], Y[j]);
				distMap[i][j] = d;
				distMap[j][i] = d;
			}
		}
	}
	void nearestNeighbor() {
		res.clear();
		vector<int> used(N, 0);
		res.push_back(0);
		used[0] = 1;
		double mn;
		int mnj;
		for (int i = 0; i < N - 1; i++) {
			mn = 1e9;
			for (int j = 0; j < N; j++) {
				if (used[j] == 0) {
					if (mn > distMap[res.back()][j]) {
						mn = distMap[res.back()][j];
						mnj = j;
					}
				}
			}
			res.push_back(mnj);
			used[mnj] = 1;
		}
	}
	void SA() {
		double score;
		score = calcScore(res);
		double T;
		double T0 = 15;
		double ti;
		double rem;
		double diff;
		int cnt = 0;
		int a, b, a1, b1;
		int l, r;
		double debugTime = 0;
		while (true) {
			if (true) {
				ti = timer.get();
				if (TIMELIMIT < ti) {
					break;
				}
				rem = (TIMELIMIT - ti) / TIMELIMIT;
				T = T0 * rem;
				if (ti > debugTime) {
					debugTime += 1.0;
					cerr << score << " " << calcScore(res) << endl;
				}
			}
			cnt++;
			a = rnd.nextInt(N);
			b = rnd.nextInt(N - 1);
			if (a <= b) b++;
			if (a > b) swap(a, b);
			if (a == 0 && b == N - 1) continue;
			a1 = a - 1;
			if (a1 == -1) a1 = N - 1;
			b1 = b + 1;
			if (b1 == N) b1 = 0;
			diff = 0;
			diff -= distMap[res[a]][res[a1]];
			diff -= distMap[res[b]][res[b1]];
			diff += distMap[res[b]][res[a1]];
			diff += distMap[res[a]][res[b1]];
			if (diff < -T * rnd.nextLog()) {
				score += diff;
				while (a < b) {
					swap(res[a], res[b]);
					a++;
					b--;
				}
			}
		}
		cerr << "cnt=" << cnt << endl;
		cerr << setprecision(15) << calcScore(res) << endl;
		cerr << setprecision(15) << score << endl;
	}
	void solve() {
		init();
		nearestNeighbor();
		SA();
	}
};
int main(int argc, char *argv[]) {
	TSP tsp;
	tsp.input();
	tsp.solve();
	tsp.output();

	return 0;
}