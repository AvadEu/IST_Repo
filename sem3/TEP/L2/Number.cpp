#include <cmath>
#include "Number.h"

#include <iostream>

const bool DEFAULT_IS_NEGATIVE = false;
const int DEFAULT_NUM_DIGITS = 0;
const int CALCULATION_BUFFER_SIZE = 16;

// Constructors & Destructors
Number::Number()
  : isNegative_(DEFAULT_IS_NEGATIVE),
    numDigits_(DEFAULT_NUM_DIGITS),
    num_(nullptr) {}

Number::Number(const int value)
  : isNegative_(value < 0),
  numDigits_(DEFAULT_NUM_DIGITS),
  num_(nullptr) {
  initializeValue(value);
}

Number::Number(const Number &other)
  : isNegative_(other.isNegative_),
  numDigits_(other.numDigits_),
  num_(nullptr) {

  if (other.num_ == nullptr) {
    throw std::invalid_argument("Cannot copy object with num_ field of nullptr!");
  }
  num_ = new int[numDigits_];
  for (int i = 0; i < numDigits_; i++) {
    num_[i] = other.num_[i];
  }
}

Number::Number(int *num, const int numDigits,const bool isNegative)
  : isNegative_(isNegative),
    numDigits_(numDigits),
    num_(num) {}

Number::~Number() {
  delete[] num_;
}

// Utility functions
void Number::parseInt(int value, int **output) const {
  *output = new int[numDigits_];
  for (int i = numDigits_ - 1; i >= 0; i--) {
    (*output)[i] = value % 10;
    value /= 10;
  }
}

int Number::calculateNumDigits(const int value) const{
  const int count = std::floor(std::log10(std::abs(value)) + 1);
  return  (count > 0) ? count : 1;
}

void Number::initializeValue(const int value) {
  if (value < 0) {
    isNegative_ = true;
  }
  numDigits_ = calculateNumDigits(std::abs(value));
  parseInt(std::abs(value), &num_);
}

int Number::countDigitsInBuffer(const int* buff) const {
  int firstNonZero = 0;
  while (firstNonZero < CALCULATION_BUFFER_SIZE - 1 && buff[firstNonZero] == 0) {
    firstNonZero++;
  }

  const int count = CALCULATION_BUFFER_SIZE - firstNonZero;

  return count;
}

std::string Number::toString() const {
  std::string output;
  for (int i = 0; i < numDigits_; i++) {
    output += std::to_string(num_[i]);
  }
  return (isNegative_ ? "-" : "") + output;
}

bool Number::firstIsBigger(const Number &first, const Number &second) const {
  bool firstIsBigger = false;
  if (first.numDigits_ > second.numDigits_) {
    firstIsBigger = true;
  } else if (first.numDigits_ < second.numDigits_) {
    firstIsBigger = false;
  } else {
    for (int i = 0; i < numDigits_; i++) {
      if (first.num_[i] > second.num_[i]) {
        firstIsBigger = true;
        break;
      }
      if (first.num_[i] < second.num_[i]) {
        firstIsBigger = false;
        break;
      }
    }
  }
  return firstIsBigger;
}

void Number::setIsNegative(const bool value) {
  isNegative_ = value;
}

// Operator overloading
Number& Number::operator=(const int value) {
  if (value == 0) {
    numDigits_ = 1;
    num_ = new int[1];
    num_[0] = 0;
    return *this;
  }
  isNegative_ = (value < 0);
  delete[] num_;
  num_ = nullptr;
  initializeValue(std::abs(value));
  return *this;
}

//Number a,b; ...
// a = b = c = d;

Number& Number::operator=(const Number &other) {
  if (this == &other) {
    return *this;
  }
  isNegative_ = other.isNegative_;
  numDigits_ = other.numDigits_;
  delete[] num_;
  num_ = new int[numDigits_];
  for (int i = 0; i < numDigits_; i++) {
    num_[i] = other.num_[i];
  }
  return *this;
}

Number Number::operator+(const Number &other) const {
  const int maxDigits = std::max(numDigits_, other.numDigits_);

  if (maxDigits + 1 > CALCULATION_BUFFER_SIZE) {
    throw std::length_error("Number is too big for buffer size of: " + std::to_string(CALCULATION_BUFFER_SIZE));
  }

  if (isNegative_ == other.isNegative_) {
    int *calcBuff = new int[CALCULATION_BUFFER_SIZE];
    int carry = 0;

    for (int i = 0; i < maxDigits; i++) {
      const int digit1 = (i < numDigits_) ? num_[numDigits_ - 1 - i] : 0;
      const int digit2 = (i < other.numDigits_) ? other.num_[other.numDigits_ - 1 - i] : 0;
      const int tmpRes = digit1 + digit2 + carry;
      calcBuff[CALCULATION_BUFFER_SIZE - i - 1] = tmpRes % 10;
      carry = tmpRes / 10;
    }

    if (carry > 0) {
      calcBuff[CALCULATION_BUFFER_SIZE - maxDigits - 1] = carry;
    }

    // Debug code
    // for (int i = 0; i < CALCULATION_BUFFER_SIZE; i++) {
    //   std::cout << calcBuff[i] << " ";
    // }

    const int resultDigitsLen = countDigitsInBuffer(calcBuff);
    const int startIndex = CALCULATION_BUFFER_SIZE - resultDigitsLen;
    int *output = new int[resultDigitsLen];

    for (int i = 0; i < resultDigitsLen; i++) {
      output[i] = calcBuff[startIndex + i];
    }
    delete[] calcBuff;

    return Number(output, resultDigitsLen, isNegative_);
  }
  const bool thisIsBigger = firstIsBigger(*this, other);

  const int* bigger = thisIsBigger ? num_ : other.num_;
  const int* smaller = thisIsBigger ? other.num_ : num_;
  const int biggerSize = thisIsBigger ? numDigits_ : other.numDigits_;
  const int smallerSize = thisIsBigger ? other.numDigits_ : numDigits_;

  int *calcBuff = new int[CALCULATION_BUFFER_SIZE];
  int borrow = 0;
  int tmpRes;

  for (int i = 0; i < maxDigits; i++) {
    int digit1 = (i < biggerSize) ? bigger[biggerSize - 1 - i] : 0;
    int digit2 = (i < smallerSize) ? smaller[smallerSize - 1 - i] : 0;

    tmpRes = digit1 - digit2 - borrow;

    if (tmpRes < 0) {
      tmpRes += 10;
      borrow = 1;
    } else {
      borrow = 0;
    }

    calcBuff[CALCULATION_BUFFER_SIZE - i - 1] = tmpRes;
  }

  const int resultDigitsLen = countDigitsInBuffer(calcBuff);
  int startIndex = CALCULATION_BUFFER_SIZE - resultDigitsLen;
  int *output = new int[resultDigitsLen];
  for (int i = 0; i < resultDigitsLen; i++) {
    output[i] = calcBuff[startIndex + i];
  }
  delete[] calcBuff;

  const bool resultIsNegative = thisIsBigger ? isNegative_ : other.isNegative_;

  return Number(output, resultDigitsLen, resultIsNegative);
}


Number Number::operator-(const Number &other) {
  const int maxDigits = std::max(numDigits_, other.numDigits_);

  if (maxDigits > CALCULATION_BUFFER_SIZE) {
    throw std::length_error("Number is too big for buffer size of: " + std::to_string(CALCULATION_BUFFER_SIZE));
  }

  if (isNegative_ != other.isNegative_) {
    Number newOther = Number(other);
    newOther.setIsNegative(true);
    isNegative_ = true;
    Number output = *this + (newOther);
    output.setIsNegative(true);
    return output;
  }

  bool const thisIsBigger = firstIsBigger(*this, other);

  const int* bigger = thisIsBigger ? num_ : other.num_;
  const int* smaller = thisIsBigger ? other.num_ : num_;
  int biggerSize = thisIsBigger ? numDigits_ : other.numDigits_;
  int smallerSize = thisIsBigger ? other.numDigits_ : numDigits_;

  int *calcBuff = new int[CALCULATION_BUFFER_SIZE];
  int borrow = 0;
  int tmpRes;

  for (int i = 0; i < maxDigits; i++) {
    const int digit1 = (i < biggerSize) ? bigger[biggerSize - 1 - i] : 0;
    const int digit2 = (i < smallerSize) ? smaller[smallerSize - 1 - i] : 0;

    tmpRes = digit1 - digit2 - borrow;

    if (tmpRes < 0) {
      tmpRes += 10;
      borrow = 1;
    } else {
      borrow = 0;
    }

    calcBuff[CALCULATION_BUFFER_SIZE - i - 1] = tmpRes;
  }

  const int resultDigitsLen = countDigitsInBuffer(calcBuff);
  int startIndex = CALCULATION_BUFFER_SIZE - resultDigitsLen;
  int *output = new int[resultDigitsLen];
  for (int i = 0; i < resultDigitsLen; i++) {
    output[i] = calcBuff[startIndex + i];
  }
  delete[] calcBuff;

  bool resultIsNegative;
  if (thisIsBigger) {
    resultIsNegative = isNegative_;
  } else {
    resultIsNegative = !isNegative_;
  }

  return Number(output, resultDigitsLen, resultIsNegative);
}

Number Number::operator*(const Number &other) const{
  const int maxResultDigits = numDigits_ + other.numDigits_;
  if (maxResultDigits > CALCULATION_BUFFER_SIZE) {
    throw std::length_error("Number is too big for buffer size of: " + std::to_string(CALCULATION_BUFFER_SIZE));
  }

  int *calcBuff = new int[CALCULATION_BUFFER_SIZE]();

  for (int i = 0; i < numDigits_; i++) {
    const int digit1 = num_[numDigits_ - 1 - i];
    int carry = 0;

    for (int j = 0; j < other.numDigits_; j++) {
      const int digit2 = other.num_[other.numDigits_ - 1 - j];
      const int pos = CALCULATION_BUFFER_SIZE - 1 - i - j;

      const int product = digit1 * digit2 + calcBuff[pos] + carry;
      calcBuff[pos] = product % 10;
      carry = product / 10;
    }

    int k = other.numDigits_;
    while (carry > 0) {
      const int pos = CALCULATION_BUFFER_SIZE - 1 - i - k;
      const int sum = calcBuff[pos] + carry;
      calcBuff[pos] = sum % 10;
      carry = sum / 10;
      k++;
    }
  }

  // Debug code
  // for (int i = 0; i < CALCULATION_BUFFER_SIZE; i++) {
  //   std::cout << calcBuff[i] << " ";
  // }

  const int resultDigitsLen = countDigitsInBuffer(calcBuff);
  const int startIndex = CALCULATION_BUFFER_SIZE - resultDigitsLen;
  int *output = new int[resultDigitsLen];
  for (int i = 0; i < resultDigitsLen; i++) {
    output[i] = calcBuff[startIndex + i];
  }
  delete[] calcBuff;

  const bool resultIsNegative = isNegative_ != other.isNegative_;

  return Number(output, resultDigitsLen, resultIsNegative);
}


Number Number::operator/(const Number &other) const {
  if (other.numDigits_ == 1 && other.num_[0] == 0) {
    throw std::invalid_argument("Division by zero");
  }

  // Copy absolute value
  Number dividend(*this);
  dividend.setIsNegative(false);

  Number divisor(other);
  divisor.setIsNegative(false);

  if (!firstIsBigger(dividend, divisor)) {
    bool equal = (dividend.numDigits_ == divisor.numDigits_);
    if (equal) {
      for (int i = 0; i < dividend.numDigits_; i++) {
        if (dividend.num_[i] != divisor.num_[i]) {
          equal = false;
          break;
        }
      }
    }

    if (equal) {
      int* output = new int[1];
      output[0] = 1;
      const bool resultSign = (isNegative_ != other.isNegative_);
      return Number(output, 1, resultSign);
    } else {
      int* output = new int[1];
      output[0] = 0;
      return Number(output, 1, false);
    }
  }

  Number quotient(0);
  const Number one(1);

  while (firstIsBigger(dividend, divisor) ||
         (dividend.numDigits_ == divisor.numDigits_ &&
          !firstIsBigger(divisor, dividend))) {
    dividend = dividend - divisor;
    quotient = quotient + one;
          }

  const bool resultSign = (isNegative_ != other.isNegative_);
  quotient.setIsNegative(resultSign);

  return quotient;
}

// Debug method
void Number::getData() const {
  std::cout << toString() << "\n";
  std::cout << isNegative_ << "\n";
  std::cout << numDigits_ << "\n";
  for (int i = 0; i < numDigits_; i++) {
    std::cout << num_[i] << "\n";
  }
}
Number Number::operator<<(const unsigned value) const {
  const int newVal = static_cast<int>(value);
  Number output =  Number(*this);
  const Number* factor = new Number(2);
  for (int i = 0; i < newVal; i++) {
    output = output * *factor;
  }
  delete factor;
  return output;
}

Number Number::operator<<(const Number &other) const {
  int otherValue = 0;
  int acc = 1;
  for (int i = other.numDigits_ - 1; i >= 0; i--) {
    otherValue = otherValue + other.num_[i] * acc;
    acc *= 10;
  }
  int *temp = new int[numDigits_];
  int k = 0;

  for (int i = otherValue; i < numDigits_; i++) {
    temp[k] = num_[i];
    k++;
  }

  for (int i = 0; i < otherValue; i++) {
    temp[k] = num_[i];
    k++;
  }

  for (int i = 0; i < numDigits_; i++) {
    num_[i] = temp[i];
  }
  return *this;
}


std::ostream& operator<<( std::ostream &os, const Number &other) {
  os << other.toString();
  return os;
}
