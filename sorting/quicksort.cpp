#include <algorithm>
#include <cassert>

int partition(int* a, int low, int high)
{
	int pivot = a[high];
	int i = low;
	for (int j = low; j < high; ++j)
	{
		if (a[j] < pivot)
		{
			std::swap(a[i], a[j]);
			++i;
		}
	}
	std::swap(a[i], a[high]);
	return i;
}

void quicksort_impl(int* a, int low, int high)
{
	if (low < high)
	{
		int p = partition(a, low, high);
		quicksort_impl(a, low, p - 1);
		quicksort_impl(a, p + 1, high);
	}
}

void quicksort(int* a, int n)
{
	quicksort_impl(a, 0, n - 1);
}

int main()
{
	int a[] = { 2, 8, 7, 1, 3, 5, 6, 4 };
	assert(!std::is_sorted(std::begin(a), std::end(a)));
	quicksort(a, std::size(a));
	assert(std::is_sorted(std::begin(a), std::end(a)));
	return 0;
}