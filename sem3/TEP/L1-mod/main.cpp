#include "Course.h"
#include "Student.h"


int main() {
    Course* course = new Course("Nowy Kurs");
    Student* s1 = new Student(1);
    Student* s2 = new Student(2);
    s1->enroll(*course);
    s2->enroll(*course);
    delete s1;

    return 0;
}