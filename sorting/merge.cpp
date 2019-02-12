#include <vector>
#include <algorithm>
#include <cassert>

// left half is  a[ beg : mid-1 ]
// right half is a[ mid : end-1 ]
// result is     b[ beg : end-1 ]
void merge(int* a, int beg, int mid, int end, int* b)
{
	int i = beg;
	int j = mid;
	for (int k = beg; k < end; ++k)
	{
		if (i < mid && (j >= end || a[i] <= a[j]))
		{
			b[k] = a[i];
			++i;
		}
		else
		{
			b[k] = a[j];
			++j;
		}
	}
}

void merge_sort_impl(int* b, int beg, int end, int* a)
{
	if (end - beg <= 1)
		return; // sorted
	auto mid = (end + beg) / 2;
	merge_sort_impl(a, beg, mid, b); // left part
	merge_sort_impl(a, mid, end, b); // right part
	merge(b, beg, mid, end, a); // merge into a
}

// top-down implementation
// copy back is avoided with alternating the direction of the merge
// with each level of recursion
void merge_sort(int* p, int n)
{
	std::vector<int> res(p, p + n); // copy
	merge_sort_impl(res.data(), 0, n, p);
}

int main()
{
	int a[] = { 2, 4, 5, 7, 1, 2, 3, 6 };
	assert(!std::is_sorted(std::begin(a), std::end(a)));
	merge_sort(a, std::size(a));
	assert(std::is_sorted(std::begin(a), std::end(a)));
	return 0;
}