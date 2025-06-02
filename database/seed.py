import random
from datetime import datetime
from faker import Faker
import logging

from db import engine, session
from models import Base, Student, Group, Teacher, Subject, Grade
from logger_config import setup_logger

logger = setup_logger()
fake = Faker()

Base.metadata.create_all(bind=engine)

try:
    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)
    session.commit()
    logger.info("Groups have been added.")

    teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
    session.add_all(teachers)
    session.commit()
    logger.info("Teachers have been added.")

    subjects = []
    for _ in range(random.randint(5, 8)):
        subject = Subject(
            name=fake.word().capitalize(), teacher=random.choice(teachers)
        )
        subjects.append(subject)
    session.add_all(subjects)
    session.commit()
    logger.info("Subjects have been added.")

    students = []
    for _ in range(random.randint(30, 50)):
        student = Student(name=fake.name(), group=random.choice(groups))
        students.append(student)
    session.add_all(students)
    session.commit()
    logger.info("Students have been added.")

    grades = []
    for student in students:
        for subject in subjects:
            for _ in range(random.randint(1, 20)):
                grade = Grade(
                    student=student,
                    subject=subject,
                    grade=random.randint(1, 100),
                    date_received=datetime.combine(
                        fake.date_this_year(), datetime.min.time()
                    ),
                )
                grades.append(grade)
    session.add_all(grades)
    session.commit()
    logger.info("Grades have been added.")

    logger.info("Database successfully seeded with random data!")

except Exception as e:
    session.rollback()
    logger.error(f"An error occurred: {e}")

finally:
    session.close()
