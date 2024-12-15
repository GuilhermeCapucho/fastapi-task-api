from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.task import Task
from pydantic import BaseModel
from typing import Optional
from auth.jwt_handler import get_current_user

router = APIRouter()

#Model para as requests
class TaskRequest(BaseModel):
    task: str
    is_completed: bool = False

class UpdateTaskRequest(BaseModel):
    task: str
    is_completed: bool

class PartialUpdateTaskRequest(BaseModel):
    task: Optional[str] = None
    is_completed: Optional[bool] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#GET - Obter tarefas
@router.get("/tasks")
def get_tasks(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.owner == current_user["username"]).all()
    
    return {"tasks": tasks}

#POST - Criar tarefa
@router.post("/tasks")
def create_task(task_request: TaskRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = Task(
        task=task_request.task,
        is_completed=task_request.is_completed,
        owner=current_user["username"]
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return {"message": "Task created successfully", "task": new_task}

#DELETE - Deletar tarefa
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner == current_user["username"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted successfully"}

#PUT - Atualizar tarefa
@router.put("/tasks/{task_id}")
def update_task(task_id: int, input: UpdateTaskRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner == current_user["username"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.task = input.task
    task.is_completed = input.is_completed
    db.commit()
    db.refresh(task)
    
    return {"message": "Task updated successfully", "task": task}

#PATCH - Atualizar parcialmente a tarefa
@router.patch("/tasks/{task_id}")
def partial_update_task(task_id: int, input: PartialUpdateTaskRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner == current_user["username"]).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if input.task is not None:
        task.task = input.task
    if input.is_completed is not None:
        task.is_completed = input.is_completed

    db.commit()
    db.refresh(task)
    
    return {"message": "Task updated partially", "task": task}