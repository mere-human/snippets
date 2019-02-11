#include <algorithm>
#include <cassert>

void insertion_sort(int* p, int n)
{
	for (int i = 1; i < n; ++i)
	{
		int j = i;
		while (j > 0 && p[j - 1] > p[j])
		{
			std::swap(p[j], p[j - 1]);
			--j;
		}
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