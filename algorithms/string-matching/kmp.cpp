#include <iostream>
#include <string>
#include <vector>

int search(const std::string &pat, const std::string &txt)
{
  const size_t m = pat.length();
  const size_t r = 128;
  // build DFA from pattern
  // array int[R][M]
  std::vector<std::vector<int>> dfa(r, std::vector<int>(m));
  dfa[pat[0]][0] = 1;
  for (int x = 0, j = 1; j < m; ++j)
  {
    // compute dfa[][j]
    for (int c = 0; c < r; ++c)
      dfa[c][j] = dfa[c][x]; // copy mismatch cases
    dfa[pat[j]][j] = j + 1;  // set match case
    x = dfa[pat[j]][x];      // update restart state
  }
  // simulate operation of DFA on txt
  {
    const int n = txt.length();
    int i = 0;
    int j = 0;
    for (; i < n && j < m; ++i)
      j = dfa[txt[i]][j];
    if (j == m)
      return i - m; // found (hit end of pattern)
  }
  return -1; // not found (hit end of text)
}

int main()
{
  std::string txt = "bcbaabacacababacaa";
  std::string pat = "ababac";
  auto pos = search(pat, txt);
  if (pos >= 0)
    std::cout << "Found at " << pos << "\n";
  else
    std::cout << "Not found\n";
  return 0;
}