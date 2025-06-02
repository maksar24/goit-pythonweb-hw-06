from sqlalchemy import func
from sqlalchemy.orm import Session
from database.db import session
from database.models import Student, Group, Teacher, Subject, Grade


def top_5_students_by_avg_grade(session: Session):
    # 5 студентів із найбільшим середнім балом з усіх предметів
    return (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )


def top_student_by_subject(session: Session, subject_name: str):
    # Студент із найвищим середнім балом з певного предмета
    return (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )


def avg_grade_by_group_and_subject(session: Session, subject_name: str):
    # Середній бал у групах з певного предмета
    return (
        session.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .all()
    )


def avg_grade_overall(session: Session):
    # Середній бал по всій таблиці оцінок
    return session.query(func.avg(Grade.grade)).scalar()


def courses_by_teacher(session: Session, teacher_name: str):
    # Курси, які читає певний викладач
    return (
        session.query(Subject.name)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .all()
    )


def students_in_group(session: Session, group_name: str):
    # Список студентів у певній групі
    return (
        session.query(Student.name).join(Group).filter(Group.name == group_name).all()
    )


def grades_in_group_by_subject(session: Session, group_name: str, subject_name: str):
    # Оцінки студентів у окремій групі з певного предмета
    return (
        session.query(Student.name, Grade.grade, Grade.date_received)
        .join(Group)
        .join(Grade)
        .join(Subject)
        .filter(Group.name == group_name, Subject.name == subject_name)
        .all()
    )


def avg_grade_given_by_teacher(session: Session, teacher_name: str):
    # Середній бал, який ставить певний викладач зі своїх предметів
    return (
        session.query(func.avg(Grade.grade))
        .join(Subject)
        .join(Teacher)
        .filter(Teacher.name == teacher_name)
        .filter(Grade.subject_id == Subject.id)
        .scalar()
    )


def courses_for_student(session: Session, student_name: str):
    # Список курсів, які відвідує певний студент
    return (
        session.query(Subject.name)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name)
        .distinct()
        .all()
    )


def courses_for_student_by_teacher(
    session: Session, student_name: str, teacher_name: str
):
    # Список курсів, які певному студенту читає певний викладач
    return (
        session.query(Subject.name)
        .join(Teacher)
        .join(Grade)
        .join(Student)
        .filter(Student.name == student_name, Teacher.name == teacher_name)
        .distinct()
        .all()
    )


if __name__ == "__main__":
    # Тестування з реальними даними із моєї бази (для тесту підставляйте дані зі своєї бази)
    try:
        print("Top 5 students by average grade:")
        for s in top_5_students_by_avg_grade(session):
            print(s)

        print("\nTop student by subject 'Nature':")
        print(top_student_by_subject(session, "Nature"))

        print("\nAverage grade by groups for subject 'Nature':")
        for g in avg_grade_by_group_and_subject(session, "Nature"):
            print(g)

        print("\nOverall average grade:")
        print(avg_grade_overall(session))

        print("\nCourses by teacher 'Amber Anthony':")
        for c in courses_by_teacher(session, "Amber Anthony"):
            print(c)

        print("\nStudents in group 'Group 1':")
        for st in students_in_group(session, "Group 1"):
            print(st)

        print("\nGrades in 'Group 1' for subject 'Develop':")
        for grade in grades_in_group_by_subject(session, "Group 1", "Develop"):
            print(grade)

        print("\nAverage grade given by teacher 'Bailey Hall':")
        print(avg_grade_given_by_teacher(session, "Bailey Hall"))

        print("\nCourses attended by student 'Kathleen Hopkins':")
        for course in courses_for_student(session, "Kathleen Hopkins"):
            print(course)

        print("\nCourses read by 'John Smith' to student 'Christopher Wood':")
        for course in courses_for_student_by_teacher(
            session, "Christopher Wood", "Zachary Gonzalez"
        ):
            print(course)

    finally:
        session.close()
