#include <iostream>
#include "solution.h"

const int ARR_FILL_VALUE_34 = 34;


bool allocTableWithFill34(const int size) {
    if (size < 0 ) {
        return false;
    }
    int *arr = new int[size];
    for (int i = 0; i < size; i++) {
        arr[i] = ARR_FILL_VALUE_34;
    }
    for (int i = 0; i < size; i++) {
        std::cout << i << ": " <<arr[i] << "\n";
    }
    delete[] arr;
    return true;
}

bool allocTable2Dim(int ***arr,const int sizeX,const int sizeY) {
    if (sizeX < 0 || sizeY < 0)
        return false;

    if (*arr == nullptr)
        return false;

    *arr = new int*[sizeX];
    for (int i = 0; i < sizeX; i++) {
        (*arr)[i] = new int[sizeY];
    }
    return true;
}

bool dealloc2DimArr(int ***arr, const int sizeX, const int sizeY) {
    if (*arr == nullptr)
        return false;

    if (sizeX < 0 || sizeY < 0) {
        return false;
    }
    for (int i = 0; i < sizeX; i++) {
        delete[] (*arr)[i];
    }
    delete[] *arr;
    return true;
}

void modTab(Table *tab, int newSize) {
    tab->setNewSize(newSize);
}

void modTab(Table tab, int newSize) {
    tab.setNewSize(newSize);
}
