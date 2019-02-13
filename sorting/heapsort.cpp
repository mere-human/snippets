#include <algorithm>
#include <cassert>

inline int left(int i)
{
	return 2 * i + 1;
}

inline int right(int i)
{
	return 2 * i + 2;
}

inline int parent(int i)
{
	return (i - 1) / 2;
}

void max_heapify(int* a, int i, const int heap_size)
{
	int l = left(i);
	int r = right(i);
	int largest = (l < heap_size && a[l] > a[i]) ? l : i;
	if (r < heap_size && a[r] > a[largest])
		largest = r;
	if (largest != i)
	{
		std::swap(a[i], a[largest]);
		max_heapify(a, largest, heap_size);
	}
}

void build_max_heap(int* a, int n)
{
	for (int i = n / 2 - 1; i >= 0; --i)
	{
		max_heapify(a, i, n);
	}
}

int main()
{
	int a[] = { 4, 1, 3, 2, 16, 9, 10, 14, 8, 7 };
	assert(!std::is_sorted(std::begin(a), std::end(a)));
	build_max_heap(a, std::size(a));
	assert(std::is_heap(std::begin(a), std::end(a)));
	//assert(std::is_sorted(std::begin(a), std::end(a)));
	return 0;
}