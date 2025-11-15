#include <string>
#include "Course.h"

#include <random>

#include "Student.h"

const std::string DEFAULT_COURSE_NAME = "";
const int MAX_DEFAULT_STUDENTS_PER_COURSE = 32;

Course::Course() {
    courseName_ = DEFAULT_COURSE_NAME;
    students_ = new Student*[MAX_DEFAULT_STUDENTS_PER_COURSE];
    enrolledStudents_ = 0;
}

Course::Course(std::string courseName) {
    students_ = new Student*[MAX_DEFAULT_STUDENTS_PER_COURSE];
    enrolledStudents_ = 0;
    courseName_ = courseName;
}

Course::~Course() {
    delete[] students_;
}

bool Course::enroll(Student &student) {
    if (enrolledStudents_ >= MAX_DEFAULT_STUDENTS_PER_COURSE)
        return false;
    students_[enrolledStudents_ + 1] = &student;
    enrolledStudents_++;
    return true;
}

bool Course::delStudent(Student* student_ptr) {
    if (student_ptr == NULL)
        return false;
    for (int i = 0; i < enrolledStudents_; i++) {
        if (students_[i] == student_ptr) {
            delete students_[i];
            students_[i] = NULL;
        }
    }
    return true;
}