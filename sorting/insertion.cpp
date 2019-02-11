#include <algorithm>
#include <cassert>

void insertion_sort(int* p, int n)
{
	for (int j = 1; j < n; ++j)
	{
		auto key = p[j];
		int i = j - 1;
		while (i >= 0 && p[i] > key)
		{
			p[i + 1] = p[i];
			--i;
		}
		p[i + 1] = key;
	}
}

int main()
{
	int a[] = { 5, 2, 4, 6, 1, 3 };
	assert(!std::is_sorted(std::begin(a), std::end(a)));
	insertion_sort(a, std::size(a));
	assert(std::is_sorted(std::begin(a), std::end(a)));
	return 0;
}