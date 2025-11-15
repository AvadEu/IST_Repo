#ifndef L1_MOD_STUDENT_H
#define L1_MOD_STUDENT_H
#include "Course.h"
class Course;

class Student {
public:
    Student();
    explicit Student(int indexNum);
    ~Student();
    void enroll(Course &course);
    void setStudentsCourse(Course* course);
private:
    int indexNum_;
    Course* studentsCourse_;
};

#endif //L1_MOD_STUDENT_H