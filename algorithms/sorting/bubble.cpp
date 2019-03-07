#include <algorithm>
#include <cassert>

void bubble_sort(int* p, int n)
{
	for (int i = 0; i < n - 1; ++i)
	{
		for (int j = n - 1; j > i; --j)
		{
			if (p[j] < p[j - 1])
				std::swap(p[j], p[j - 1]);
		}
	}
}

int main()
{
	int a[] = { 5, 2, 4, 6, 1, 3 };
	assert(!std::is_sorted(std::begin(a), std::end(a)));
	bubble_sort(a, std::size(a));
	assert(std::is_sorted(std::begin(a), std::end(a)));
	return 0;
}