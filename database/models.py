from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, DateTime
from datetime import datetime

Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    students: Mapped[list["Student"]] = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id"))

    group: Mapped["Group"] = relationship("Group", back_populates="students")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    subjects: Mapped[list["Subject"]] = relationship(
        "Subject", back_populates="teacher"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id"))

    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id"))
    subject_id: Mapped[int | None] = mapped_column(ForeignKey("subjects.id"))
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    date_received: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="grades")
