#pragma once
#include <vector>

#ifndef L4_RESULT_H
#define L4_RESULT_H

template <typename T, typename E>
class Result {
public:
  Result(): value_ptr(nullptr) {};

  explicit Result(const T& val) : value_ptr(new T(val)) {};

  explicit Result(const E* err) : value_ptr(nullptr) {
    if (err != nullptr) {
      errors_.push_back(new E(*err));
    }
  }

  explicit Result(std::vector<E*> errs) : value_ptr(nullptr) {
    for (int i = 0; i < errs.size(); i++) {
      errors_.push_back(new E(*errs[i]));
    }
  }

  Result(const Result<T, E>& other) {
    copyFrom(other);
  }

  ~Result() {
    clear();
  }

  Result<T, E>& operator=(const Result<T, E>& other) {
    if (this != &other) {
      clear();
      copyFrom(other);
    }
    return *this;
  }


  static Result<T, E> ok(const T& val) {
    return Result<T, E>(val);
  }

  static Result<T, E> fail(E* error) {
    return Result<T, E>(error);
  }

  static Result<T, E> fail(std::vector<E*>& errs) {
    return Result<T, E>(errs);
  }

  bool isSuccess() const {
    return value_ptr != nullptr && errors_.empty();
  }

  T getValue() const {
    if (value_ptr != nullptr) return *value_ptr;
    return T();
  }

  std::vector<E*>& getErrors() {
    return errors_;
  }

private:
  T* value_ptr;
  std::vector<E*> errors_;

  void clear() {
    if (value_ptr != nullptr) {
      delete value_ptr;
      value_ptr = nullptr;
    }
    for (size_t i = 0; i < errors_.size(); i++) {
      delete errors_[i];
    }
    errors_.clear();
  }

  void copyFrom(const Result<T, E>& other) {
    if (other.value_ptr != nullptr) {
      value_ptr = new T(*other.value_ptr);
    } else {
      value_ptr = nullptr;
    }
        
    for (size_t i = 0; i < other.errors_.size(); i++) {
      errors_.push_back(new E(*other.errors_[i]));
    }
  }
};


template <typename E>
class Result<void, E> {
public:
    Result() = default;

    explicit Result(E* pcError) {
        if (pcError != nullptr) errors_.push_back(pcError);
    }

    explicit Result(std::vector<E*>& vErrors) {
        for (size_t i = 0; i < vErrors.size(); i++) {
            errors_.push_back(new E(*vErrors[i]));
        }
    }

    Result(const Result<void, E>& cOther) {
        vCopyFrom(cOther);
    }

    ~Result() {
        vClear();
    }

    Result<void, E>& operator=(const Result<void, E>& cOther) {
        if (this != &cOther) {
            vClear();
            vCopyFrom(cOther);
        }
        return *this;
    }

    static Result<void, E> cOk() {
        return Result<void, E>();
    }

    static Result<void, E> cFail(E* pcError) {
        return Result<void, E>(pcError);
    }

    static Result<void, E> cFail(std::vector<E*>& vErrors) {
        return Result<void, E>(vErrors);
    }

    bool bIsSuccess() const {
        return errors_.empty();
    }

    std::vector<E*>& vGetErrors() {
        return errors_;
    }

private:
    std::vector<E*> errors_;

    void vClear() {
        for (size_t i = 0; i < errors_.size(); i++) {
            delete errors_[i];
        }
        errors_.clear();
    }

    void vCopyFrom(const Result<void, E>& cOther) {
        for (size_t i = 0; i < cOther.errors_.size(); i++) {
            errors_.push_back(new E(*cOther.errors_[i]));
        }
    }
};


#endif //L4_RESULT_H