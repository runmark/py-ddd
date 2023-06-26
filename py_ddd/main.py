from typing import ForwardRef, List, Optional
from fastapi import FastAPI

from pydantic import BaseModel


class Person(BaseModel):
    id: int
    name: str
    email: str
    team: ForwardRef("Team") = None  # 引用Team模型的ForwardRef


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str = "TODO"
    assignee: Person = None


class Team(BaseModel):
    id: int
    name: str
    members: List[Person] = []


Person.update_forward_refs()

# create some example tasks
tasks: List[Task] = []
user1 = Person(id=1, name="Alice", email="alice@example.com", team=None)
task1 = Task(
    id=1,
    title="Implement login page",
    description="Create a login page for the website",
    status="TODO",
    assignee=user1,
)
tasks.append(task1)
user2 = Person(id=2, name="Bob", email="bob@example.com", team=None)
task2 = Task(
    id=2,
    title="Implement registration page",
    description="Create a registration page for the website",
    status="TODO",
    assignee=user2,
)
tasks.append(task2)

app = FastAPI()


@app.get("/tasks")
async def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return None


@app.post("/tasks")
async def post_tasks(task: Task):
    tasks.append(task)
    return task
