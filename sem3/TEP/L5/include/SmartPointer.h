#pragma once
#include "RefCounter.h"
#include <iostream> // Do wypisywania logów (opcjonalne)
#include <utility>  // std::move

template <typename T>
class SmartPointer {
public:

    explicit SmartPointer(T* ptr = nullptr) {
        pointer = ptr;
        if (ptr != nullptr) {
            counter = new RefCounter();
            counter->add();
        } else {
            counter = nullptr;
        }
    }

    SmartPointer(const SmartPointer& other) {
        pointer = other.pointer;
        counter = other.counter;
        if (counter) {
            counter->add();
        }
    }

    SmartPointer(SmartPointer&& other) noexcept {
        pointer = other.pointer;
        counter = other.counter;
        
        other.pointer = nullptr;
        other.counter = nullptr;
    }

    ~SmartPointer() {
        cleanup();
    }

    SmartPointer& operator=(const SmartPointer& other) {
        if (this == &other) {
            return *this;
        }

        cleanup();

        pointer = other.pointer;
        counter = other.counter;

        if (counter) {
            counter->add();
        }

        return *this;
    }

    SmartPointer& operator=(SmartPointer&& other) noexcept {
        if (this == &other) {
            return *this;
        }

        cleanup();

        pointer = other.pointer;
        counter = other.counter;

        other.pointer = nullptr;
        other.counter = nullptr;

        return *this;
    }

    T& operator*() { return *pointer; }
    T* operator->() { return pointer; }

    int getCount() const {
        return counter ? counter->get() : 0;
    }

private:
    T* pointer;
    RefCounter* counter;

    void cleanup() const {
        if (counter) {
            if (counter->dec() == 0) {
                delete pointer;
                delete counter;
            }
        }
    }
};