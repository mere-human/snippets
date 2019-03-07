#include <string>
#include <iostream>

int search(const std::string &pat, const std::string &txt)
{
    int m = pat.length();
    int n = txt.length();
    int i = 0; // points to the end of sequence of already-matched characters
    int j = 0;
    for (; i < n && j < m; ++i)
    {
        if (txt[i] == pat[j])
        {
            ++j;
        }
        else
        {
            // mismatch - backup
            i -= j;
            j = 0;
        }
    }

    if (j == m)
        return i - m; // found
    return -1;        // not found
}

int main()
{
    std::string txt = "abacadabrac";
    std::string pat = "abra";
    auto pos = search(pat, txt);
    if (pos >= 0)
        std::cout << "Found at " << pos << "\n";
    else
        std::cout << "Not found\n";
    return 0;
}