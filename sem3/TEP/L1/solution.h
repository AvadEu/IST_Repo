#ifndef L1_SOLUTION_H
#define L1_SOLUTION_H
#include "Table.h"

bool allocTableWithFill34(int size); // Zad1
bool allocTable2Dim(int ***arr, int sizeX, int sizeY); // Zad2
bool dealloc2DimArr(int ***arr, int sizeX, int sizeY);

void modTab(Table *tab, int newSize);
void modTab(Table tab, int newSize);

#endif //L1_SOLUTION_H