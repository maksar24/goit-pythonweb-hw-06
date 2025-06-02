from database.db import session as my_session
from database.models import Student, Group, Teacher, Subject


def print_all_groups(session):
    print("Groups:")
    groups = session.query(Group.name).all()
    for g in groups:
        print(f"- {g.name}")


def print_all_students(session):
    print("Students:")
    students = session.query(Student.name).all()
    for s in students:
        print(f"- {s.name}")


def print_all_teachers(session):
    print("Teachers:")
    teachers = session.query(Teacher.name).all()
    for t in teachers:
        print(f"- {t.name}")


def print_all_subjects(session):
    print("Subjects:")
    subjects = session.query(Subject.name).all()
    for sub in subjects:
        print(f"- {sub.name}")


if __name__ == "__main__":
    try:
        print_all_groups(my_session)
        print()
        print_all_students(my_session)
        print()
        print_all_teachers(my_session)
        print()
        print_all_subjects(my_session)
    finally:
        my_session.close()
