#pragma once
#include <string>

#ifndef L1_CTABLE_H
#define L1_CTABLE_H

class Table {
public:
    Table();
    Table(std::string name, int tableLen);
    Table(Table &other);
    ~Table();
    void setName(std::string name);
    bool setNewSize(int size);
    Table* clone();
private:
    std::string name_;
    int size_;
    int * data_;
};

#endif //L1_CTABLE_H