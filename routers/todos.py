from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from models import Todo, TodoCreate, TodoUpdate
from database import todos
from config import settings

router = APIRouter()

@router.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    new_todo = Todo(title=todo.title, description=todo.description)
    todos[new_todo.id] = new_todo
    return new_todo

@router.get("/todos", response_model=List[Todo])
async def read_todos(skip: int = 0, limit: int = settings.items_per_page, completed: Optional[bool] = None):
    filtered_todos = list(todos.values())
    if completed is not None:
        filtered_todos = [todo for todo in filtered_todos if todo.completed == completed]
    return filtered_todos[skip : skip + limit]

@router.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todos[todo_id]

@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    existing_todo = todos[todo_id]
    update_data = todo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_todo, key, value)
    existing_todo.updated_at = datetime.now()
    return existing_todo

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str):
    if todo_id not in todos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    del todos[todo_id]
    return