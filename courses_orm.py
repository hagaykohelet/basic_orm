from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, select


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    hours: int
    is_active: bool = True


engine = create_engine("sqlite:///courses.db", echo=True)


def create_db_and_table() -> None:
    SQLModel.metadata.create_all(engine)


def add_course(name: str, hours: int, is_active: bool = True) -> None:
    course = Course(name=name, hours=hours, is_active=is_active)
    with Session(engine) as session:
        session.add(course)
        session.commit()
        session.refresh(course)
        print(f"add course with id={course.id}")


def get_active_courses() -> list[Course]:
    with Session(engine) as session:
        statement = select(Course).where(Course.is_active == True)
        results = session.exec(statement)
        courses = results.all()
        return courses


if __name__ == "__main__":
    create_db_and_table()
    add_course("sql basics", 20, True)
    add_course("python intro", 30, True)
    add_course("legacy system", 10, False)
    active = get_active_courses()
    print("active courses")
    for course in active:
        print(f"{course.id}: {course.name} hours active = {course.is_active}")
