#include <iostream>
#include "solution.h"
#include "Table.h"

int main() {
    allocTableWithFill34(4);

    int **arr;
    allocTable2Dim(&arr, 3, 3);
    dealloc2DimArr(&arr, 3, 3);

    // Table *tab1 = new Table("tab", 10);
    // Table tab2("tab2", 10);
    // modTab(tab1, 20);
    // modTab(tab2, 20);

    int tabArrSize = 2;
    Table **tab3 = new Table*[tabArrSize];
    for (int i = 0; i < tabArrSize; i++) {
        tab3[i] = new Table("tab" + std::to_string(i + 10), i);
    }
    tab3[0]->setNewSize(10);
    (*tab3[1]).setNewSize(10);

    delete tab3[0];
    delete tab3[1];
    delete[] tab3;

    return 0;
}