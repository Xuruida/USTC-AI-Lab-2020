#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>

void print_matrix(int matrix[][9])
{
    std::cout << "Matrix:" << std::endl;
    for (int i = 0; i < 9; i++)
    {
        for (int j = 0; j < 9; j++)
            std::cout << matrix[i][j] << '\t';
        std::cout << std::endl;
    }
}
inline bool checkNum(int num, int x, int y, int matrix[][9])
{
    for (int i = 0; i < 9;i++)
        if (matrix[x][i] == num || matrix[i][y] == num)
            return false;
    int rpos = 3 * (x / 3), cpos = 3*(y / 3);
    for (int i = 0; i < 3;i++)
        for (int j = 0; j < 3;j++)
            if (matrix[rpos + i][cpos + j] == num)
                return false;
    if (x == y)
        for (int i = 0; i < 9; i++)
            if (matrix[i][i] == num)
                return false;
    if (x == 8-y)
        for (int i = 0; i < 9;i++)
            if (matrix[i][8-i] == num)
                return false;
    return true;
}

inline bool isValid(int matrix[][9])
{
    int col[10] = {0}, row[10] = {0};
    int diag1[10] = {0}, diag2[10] = {0};
    for (int i = 0; i < 9; i++)
    {
        memset(col, 0, sizeof(col));
        memset(row, 0, sizeof(row));
        for (int j = 0; j < 9; j++)
        {
            col[matrix[j][i]]++;
            row[matrix[i][j]]++;
        }
        for (int j = 1; j <= 9;j++)
            if (col[j] > 1 || row[j] > 1)
                return false;
    }
    for (int i = 0; i < 9;i++)
    {
        diag1[matrix[i][i]]++;
        diag2[matrix[8 - i][i]]++;
    }
    for (int i = 1; i <= 9;i++)
    {
        if (diag1[i]>1 || diag2[i]>1)
            return false;
    }
    return true;
}

bool backtracking_search(int matrix[][9], int x, int y)
{
    // print_matrix(matrix);
    bool bo = false;
    for (; x < 9; x++)
    {
        for (; y < 9; y++)
            if (matrix[x][y] == 0)
            {
                bo = true;
                break;
            }
        if (bo)
            break;
        y = 0;
    }
    if (x >= 9)
        return true;

    for (int tryNum = 1; tryNum <= 9; tryNum++)
    {
        if (checkNum(tryNum, x, y, matrix))
        {
            matrix[x][y] = tryNum;
            if (backtracking_search(matrix, x, y)) return true;
            matrix[x][y] = 0;
        }
    }

    return false;
}

void init(char *inputName)
{
    FILE *fpin;
    char path[100] = "../input/";
    
    // Read data
    strcat(path, inputName);
    if (!(fpin = fopen(path, "r+")))
    {
        printf("Cannot open input file!");
        exit(-1);
    }

    int matrix[9][9];
    for (int i = 0; i < 9; i++)
        for (int j = 0; j < 9; j++)
            fscanf(fpin, "%d", &matrix[i][j]);

    if (!isValid(matrix))
    {
        printf("Input matrix invalid\n");
        return;
    }
    if (!backtracking_search(matrix, 0, 0))
    {
        printf("NO Possible result\n");
        return;
    }
    else
        print_matrix(matrix);
}

int main(int argv, char **argc)
{
    if (argc[1] == nullptr)
    {
        printf("Please specify input file!");
        exit(-1);
    }
    init(argc[1]);
    return 0;
}