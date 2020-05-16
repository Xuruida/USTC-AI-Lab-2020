#include<iostream>
#include<cstdio>
#include<queue>
#include<algorithm>
#include<cstdlib>
#include<cstring>
#include<list>
#include<time.h>

clock_t start_time;
#define CHECK_EQUAL_MAX_DEPTH 50
#define STEP_COST 10

const int g_weight[] = {
    0,
    10,  10, 10, 10, 10,
    10,  10, 10, 10, 10,
             10, 10, 10,
    10,  10, 10, 10, 10,
    10,  10, 10
};

struct position
{
    int x, y;
};

typedef struct Node
{
    int state[5][5];
    struct position sevenPos = {-1, -1};
    int fValue = 0, gValue = 0, hValue = 0;
    struct Node *parent = nullptr;

    char direction = 'u';
    int num = 0;
} Node;

const struct position final_pos[] =
{
    {0, 0},
    {0, 0}, {0, 1}, {0, 2}, {0, 3}, {0, 4},
    {2, 0}, {1, 0}, {1, 2}, {1, 3}, {1, 4},
                    {2, 2}, {2, 3}, {2, 4},
    {3, 0}, {3, 1}, {3, 2}, {3, 3}, {3, 4},
    {4, 0}, {4, 1}, {4, 2}
};

const struct position move_arr[] = {
    {1, 0},
    {0, -1},
    {-1, 0},
    {0, 1}
};

const char dir_char[] = {'u', 'r', 'd', 'l'};

struct node_cmp
{
    bool operator() (Node *a, Node *b)
    {
        return a->fValue > b->fValue;
    }
};

inline int max(int a, int b)
{
    return a > b ? a : b;
}
// Calculate Manhattan Distance Sum of node.
int calc_node_value(Node *node, int gValue){
    int tmp = 0, pos;
    struct position sevenPos = {-1, -1};

    // Assign G Value.
    node->gValue = gValue;

    // Calculate H Value.
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++)
            if ((pos = node->state[i][j]) != 0)
            {
                if (sevenPos.x == -1 && pos == 7)
                {
                    sevenPos.x = i, sevenPos.y = j;
                    tmp += g_weight[pos] * (abs(final_pos[pos].x - i) + abs(final_pos[pos].y - j));
                    // tmp += g_weight[pos] * (max(abs(final_pos[pos].x - i), abs(final_pos[pos].y - j)));
                
                }
                else if (pos != 7)
                    tmp += g_weight[pos] * (abs(final_pos[pos].x - i) + abs(final_pos[pos].y - j));
                    // tmp += g_weight[pos] * (max(abs(final_pos[pos].x - i), abs(final_pos[pos].y - j)));
            }
    node->hValue = tmp;

    // Calculate F Value.
    node->fValue = node->gValue + node->hValue;

    // Assign 7 Position
    node->sevenPos = sevenPos;

    return node->fValue;
}

void print_node(Node *node)
{
    printf("Node:\n\nState:\n");
    for (int i = 0; i < 5; i++)
    {
        for (int j = 0; j < 5; j++)
            printf("%d\t", node->state[i][j]);
        printf("\n");
    }
    printf("\nSevenPos: (%d, %d)\n", node->sevenPos.x, node->sevenPos.y);
    printf("\nfValue: %d\ngValue: %d\nhValue: %d\n================================\n", node->fValue, node->gValue, node->hValue);
}

int step = 0;
void print_res(Node *node)
{
    if (node->parent)
        step++, print_res(node->parent);
    // print_node(node);
    else
    {
        printf("\nResult:\nTotal Step(s): %d\nDetail:\n", step);
        return;
    }
    printf("(%d, %c)\n", node->num, node->direction);
    // print_node(node);
}

#define CHECK(X, Y, N) (isValid((X), (Y)) && N->state[(X)][(Y)] == 0)

std::priority_queue<Node *, std::vector<Node *>, node_cmp> nodePQueue;
std::vector<Node *> closedVec;
int minH = 2147483647;

inline bool isValid(int x, int y)
{
    return (x < 5) && (x >= 0) && (y < 5) && (y >= 0);
}

bool isEqual(Node *a, Node *b)
{
    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++)
            if (a->state[i][j] != b->state[i][j])
                return false;
    return true;
}

bool haveVisited(Node *node)
{
    for(auto i: closedVec)
    {
        if (isEqual(node, i))
            return true;
    }
    return false;
}

void init(char *fileName)
{
    Node *initNode;
    FILE *fpin;
    char path[256] = "../input/";
    strcat(path, fileName);
    if (!(fpin = fopen(path, "r+")))
        exit(-1);

    initNode = new Node;
    for (int i = 0; i < 5; i++)
    {
        fscanf(fpin, "%d,%d,%d,%d,%d", 
            &initNode->state[i][0],
            &initNode->state[i][1],
            &initNode->state[i][2],
            &initNode->state[i][3],
            &initNode->state[i][4]);
    }
    calc_node_value(initNode, 0);
    print_node(initNode);
    closedVec.emplace_back(initNode);
    nodePQueue.emplace(initNode);
}

int makeNode (Node *src, Node *dest,
              int x, int y, int moveType)
{
    int state[5][5];

    dest->parent = src;

    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++)
            state[i][j] = src->state[i][j];

    bool isSeven = (state[x][y] == 7);

    if (isSeven)
    {
        if (moveType == 0)
        {
            state[x - 1][y] = 7, state[x - 1][y + 1] = 7;
            state[x][y] = 0, state[x + 1][y + 1] = 0;
        }
        else if (moveType == 1)
        {
            state[x][y] = 0, state[x + 1][y + 1] = 0;
            state[x][y + 2] = 7, state[x + 1][y + 2] = 7;
        }
        else if (moveType == 2)
        {
            state[x][y] = 0, state[x][y + 1] = 0;
            state[x + 1][y] = 7, state[x + 2][y + 1] = 7;
        }
        else if (moveType == 3)
        {
            state[x][y + 1] = 0, state[x + 1][y + 1] = 0;
            state[x][y - 1] = 7, state[x + 1][y] = 7;
        }
        dest->num = 7;
        dest->direction = dir_char[moveType];
    }
    else
    {
        dest->num = state[x][y];
        dest->direction = dir_char[moveType];
        state[x - move_arr[moveType].x][y - move_arr[moveType].y] = state[x][y];
        state[x][y] = 0;
    }

    for (int i = 0; i < 5; i++)
        for (int j = 0; j < 5; j++)
            dest->state[i][j] = state[i][j];

    // node *p = src;
    // int depth = 1;
    // while (p && depth <= CHECK_EQUAL_MAX_DEPTH)
    // {
    //     if (isEqual(p, dest))
    //         return -1;
    //     p = p->parent;
    //     depth++;
    // }

    if (haveVisited(dest))
        return -1;

    closedVec.emplace_back(dest);

    calc_node_value(dest, src->gValue + STEP_COST);
    if (dest->hValue == 0)
    {
        printf("Find Result!\n");
        print_node(dest);
        print_res(dest);
        time_t stop_time = clock();
        printf("Searching takes: %.5lf seconds\n", (double)(stop_time - start_time) / CLOCKS_PER_SEC);
        exit(0);
    }
    return 0;
}

// A* Search
void search()
{
    Node *now, *nextNode;
    int index = 1;
    int status;

    while (!nodePQueue.empty())
    {
        now = nodePQueue.top();
        nodePQueue.pop();
        index++;
        if (now->hValue <= minH)
        {
            minH = now->hValue;
            printf("\nIndex: %d\n", index);
            print_node(now);
        }
        else if (index % 5000 == 0)
        {
            printf("\n-----NOT MINH-----     Current minH = %d\nIndex: %d\n", minH, index);
            print_node(now);
        }
        // try to move '7' block
        bool canMoveSeven = true;
        int sevenX = now->sevenPos.x, sevenY = now->sevenPos.y;
        nextNode = new Node;
        if (CHECK(sevenX - 1, sevenY, now) && CHECK(sevenX - 1, sevenY + 1, now))
            // (7, 0)
            status = makeNode(now, nextNode, sevenX, sevenY, 0);
        else if (CHECK(sevenX, sevenY + 2, now) && CHECK(sevenX + 1, sevenY + 2, now))
            // (7, 1)
            status = makeNode(now, nextNode, sevenX, sevenY, 1);
        else if (CHECK(sevenX + 1, sevenY, now) && CHECK(sevenX + 2, sevenY + 1, now))
            // (7, 2)
            status = makeNode(now, nextNode, sevenX, sevenY, 2);
        else if (CHECK(sevenX, sevenY - 1, now) && CHECK(sevenX + 1, sevenY, now))
            // (7, 3)
            status = makeNode(now, nextNode, sevenX, sevenY, 3);
        else
            canMoveSeven = false;

        if (canMoveSeven && status != -1)
            nodePQueue.emplace(nextNode);
        else
            delete nextNode;

        // move single blocks
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 5; j++)
                if (now->state[i][j] == 0)
                {
                    for (int k = 0; k < 4; k++)
                    {
                        int testX, testY;
                        testX = i + move_arr[k].x, testY = j + move_arr[k].y;
                        if (isValid(testX, testY) && 
                            now->state[testX][testY] != 0 &&
                            now->state[testX][testY] != 7)
                        {
                            // (state[testX][testY], k)
                            nextNode = new Node;
                            if (makeNode(now, nextNode, testX, testY, k)!=-1)
                                nodePQueue.emplace(nextNode);
                            else
                                delete nextNode;
                        }
                    }
                }
    }
    printf("NO Possible solution found!\n");
}

int main(int argc, char **argv)
{
    init(argv[1]);
    start_time = clock();
    search();
    return 0;
}