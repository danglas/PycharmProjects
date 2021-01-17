# Write your code here

from sqlalchemy import create_engine
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

rows = session.query(Table).all()

menu = "1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit"
print(menu)

menu_choice = input()

while menu_choice != '0':
    if menu_choice == '1':
        print("Today:")
        today = datetime.today()
        rows_today = session.query(Table).filter(Table.deadline == today.date()).all()
        if not rows_today:
            print('Nothing to do today!')
        else:
            for i in rows_today:
                print(i.task)
    elif menu_choice == '2':
        x=0
        task_number = 1
        today = datetime.today()
        while x < 7:
            print((today + timedelta(days=x)).strftime('%A'), end=" ")
            print((today + timedelta(days=x)).day, end=" ")
            print((today + timedelta(days=x)).strftime('%b') + ":")

            day_of_7 = today + timedelta(days=x)
            daily_tasks = session.query(Table).filter(Table.deadline == day_of_7.date()).all()
            if not daily_tasks:
                print("Nothing to do!") # if no tasks for that day
            for i in daily_tasks:
                print(str(task_number) + ". " + i.task)
                task_number = task_number + 1
            print("") # add line between days
            task_number = 1  # reset to 1
            x = x + 1
    elif menu_choice == '3':
        task_number = 1

        if not rows:
            print('Nothing to do!')
        else:
            print("All tasks:")
            rows = session.query(Table).order_by(Table.deadline).all()
            for i in rows:
                print(str(task_number) + ". " + i.task + ".", end=" ")
                print(i.deadline.day, end=" ")
                print(i.deadline.strftime('%b'))
                task_number += 1
        print("")
    elif menu_choice == '4':
        task_number = 1
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        print("Missed tasks:")
        if not rows:
            print('Nothing is missed!')
        else:
            for i in rows:
                print(str(task_number) + ". " + i.task + ".", end=" ")
                print(i.deadline.day, end=" ")
                print(i.deadline.strftime('%b'))
                task_number += 1
        print("")
        print(menu)
    elif menu_choice == '5':
        print("Enter task")
        task = input()
        print("Enter deadline")
        task_date = input()
        task_date = datetime.strptime(task_date, '%Y-%m-%d')
        new_row = Table(task=task, deadline=task_date)
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')
        print(menu)
    elif menu_choice == '6':
        print("Choose the number of the task you want to delete:")
        task_number = 1
        rows = session.query(Table).order_by(Table.deadline).all()
        for i in rows:
            print(str(task_number) + ". " + i.task + ".", end=" ")
            print(i.deadline.day, end=" ")
            print(i.deadline.strftime('%b'))
            task_number += 1

        row_index = int(input()) - 1
        specific_row = rows[row_index]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!\n")
        print(menu)

    menu_choice = input()
    if menu_choice == '0':
        print('Bye!')
