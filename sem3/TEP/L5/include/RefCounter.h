#pragma once

class RefCounter {
public:
  RefCounter();
  int add();
  int dec();
  int get() const;

private:
  int count;
};