#ifndef L1_MOD_COURSE_H
#define L1_MOD_COURSE_H
#include <string>
#include "Student.h"
class Student;

class Course {
public:
    Course();
    explicit Course(std::string courseName);
    ~Course();
    bool enroll(Student &student);
    bool delStudent(Student* student_ptr);


private:
    std::string courseName_;
    Student** students_;
    int enrolledStudents_;
};
#endif //L1_MOD_COURSE_H