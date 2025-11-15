#pragma once
#include <iostream>
#include "Table.h"

const int DEFAULT_TABLE_LEN = 10;
const std::string DEFAULT_TABLE_NAME= "Table";
const std::string DEFAULT_CONSTRUCTOR_MSG = "bezp: ";
const std::string PARAMETER_CONSTRUCTOR_MSG = "parametr: ";
const std::string COPY_CONSTRUCTOR_MSG = "kopiuj: ";
const std::string DESTRUCTOR_MSG = "usuwam: ";
const std::string COPY_CONSTRUCTOR_SUFFIX = "_copy";


Table::Table() {
    name_ = DEFAULT_TABLE_NAME;
    size_ = 0;
    data_ = new int[DEFAULT_TABLE_LEN];
    std::cout << DEFAULT_CONSTRUCTOR_MSG << name_ << "\n";
}

Table::Table(std::string name, const int tableLen) {
    name_ = name;
    size_ = tableLen;
    data_ = new int[size_];
    std::cout << PARAMETER_CONSTRUCTOR_MSG << name_ << "\n";
}

Table::Table(Table &other) {
    size_ = other.size_;
    name_ = other.name_ + COPY_CONSTRUCTOR_SUFFIX;
    data_ = new int[other.size_];
    for (int i = 0; i < size_; i++) {
        data_[i] = other.data_[i];
    }
    std::cout << COPY_CONSTRUCTOR_MSG << name_ << "\n";
}


void Table::setName(std::string name) {
    name_ = name;
}

bool Table::setNewSize(const int size) {
    if (size < 0 || size < size_) {
        return false;
    }
    size_ = size;
    return true;
}

Table::~Table() {
    delete[] data_;
    std::cout << DESTRUCTOR_MSG << name_ << "\n";
}

Table *Table::clone() {
    return new Table(*this);
}
