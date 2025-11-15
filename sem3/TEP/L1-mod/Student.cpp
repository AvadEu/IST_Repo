#include "Student.h"
#include "Course.h"
#include <iostream>
#include <ostream>

const int DEFAULT_INDEX_NUM = 0;

Student::Student() {
    indexNum_ = DEFAULT_INDEX_NUM;
}

Student::Student(int indexNum) {
    indexNum_ = indexNum;
}

Student::~Student() {
    studentsCourse_->delStudent(this);
}

void Student::setStudentsCourse(Course *course) {
    studentsCourse_ = course;
}



void Student::enroll(Course &course) {
    const bool flag = course.enroll(*this);
    if (flag) {
        studentsCourse_ = &course;
        std::cout << "Student " << indexNum_ << " enrolled in course \n";
    }
    else {
        std::cout << "Student " << indexNum_ << " cannot be enrolled in course \n";
    }
}