# Write your code here
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker

# create db
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
# create Base class
Base = declarative_base()


# table (Model class)
class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


# create table in db
Base.metadata.create_all(engine)
# create session object to manage db
Session = sessionmaker(bind=engine)
session = Session()


# new_row = Table(string_field = 'This is string field!', date_field = datetime.strptime('09-07-2020','%m-%d-%Y').date())
# session.add(new_row)
# session.commit()
def today_task():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today).all()
    print(f"Today {today.day} {today.strftime('%b')}: ")
    if rows == []:
        print('Nothing to do!')
    else:
        for i in range(len(rows)):
            print(f"{rows[i].id}. {rows[i].task}")


def week_task():
    today = datetime.today()
    rows = session.query(Table).all()
    weekday = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
    for i in range(7):
        calendar = today + timedelta(days = i)
        print(f"{weekday[calendar.weekday()]} {calendar.day} {calendar.strftime('%b')}: ")
        flag = 0
        for j in range(len(rows)):
            if rows[j].deadline == calendar.date():
                print(f"{rows[j].id}. {rows[j].task}")
                flag = 1
        if flag == 0:
            print("Nothing to do!")
        print()


def all_task():
    session.query(Table).order_by(Table.deadline).all()
    rows = session.query(Table).all()
    print("All tasks:")
    if rows == []:
        print("Nothing to do!")
    else:
        for i in range(len(rows)):
            print(f"{rows[i].id}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")


def missed_task():
    session.query(Table).order_by(Table.deadline).all()
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    print("Missed Tasks:")
    if rows == []:
        print("Nothing is missed!")
    else:
        for i in range(len(rows)):
            print(f"{rows[i].id}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")

def delete_task():
    print("Choose the number of the task you want to delete: ")
    all_task()
    n = int(input())
    rows = session.query(Table).all()
#    if rows == []:
#    	print("Deletion is not possible!")
#    else:
    session.delete(rows[n-1])
    session.commit()
    print("The task has been deleted!")


def add_task():
    print("Enter Task")
    task = input()
    print("Enter deadline")
    date_str = input()
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')  # return a datetime corresponding to date_string, parsed
    # according to format.
    # Format example: '%Y-%m-%d' - '2020-04-24'
    new_row = Table(task=task, deadline=date_obj)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


while True:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    n = int(input())
    if n == 1:
        today_task()
        print()
    elif n == 2:
        week_task()
        print()
    elif n == 3:
        all_task()
        print()
    elif n == 4:
        missed_task()
        print()
    elif n == 5:
        add_task()
        print()
    elif n == 6:
        delete_task()
        print()
    else:
        print("Bye!")
        exit()

