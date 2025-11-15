#pragma once

#include <string>

#ifndef L2_NUMBER_H
#define L2_NUMBER_H

class Number {
public:
  Number();
  explicit Number(int value);
  Number(int *num, int numDigits, bool isNegative);
  Number(const Number &other);
  ~Number();
  std::string toString() const;
  Number &operator=(int value);
  Number &operator=(const Number &other);
  Number operator+(const Number &other) const;
  Number operator-(const Number &other);
  Number operator*(const Number &other) const;
  Number operator/(const Number &other) const;
  Number operator<<( unsigned value) const;
  Number operator<<(const Number &other) const;
  friend std::ostream& operator<<(std::ostream &os, const Number &other);
  void getData() const;
private:
  bool firstIsBigger(const Number &first,const Number &second) const;
  void initializeValue(int value);
  void parseInt(int value, int **output) const;
  int calculateNumDigits(int value) const;
  int countDigitsInBuffer(const int* buff) const;
  void setIsNegative(bool value);
  bool isNegative_;
  int numDigits_;
  int *num_;
};

#endif //L2_NUMBER_H