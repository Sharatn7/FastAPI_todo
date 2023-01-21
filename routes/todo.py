from typing import List
from beanie import PydanticObjectId
from database.connection import Database
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from models.todo import Todo
from fastapi.responses import RedirectResponse


todo_router = APIRouter(tags=["Todos"])
todo_database = Database(Todo)
templates = Jinja2Templates(directory="templates/")


@todo_router.post("/")
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    await todo_database.save(todo)
    tasks = await todo_database.get_all()
    return templates.TemplateResponse("todos.html",
                                      {
                                          "request": request,
                                          "tasks": tasks
                                      })


@todo_router.get("/", response_model=List[Todo])
async def retrieve_all_todos(request: Request) -> List[Todo]:
    tasks = await todo_database.get_all()
    return templates.TemplateResponse("todos.html",
                                      {
                                          "request": request,
                                          "tasks": tasks
                                      })


@todo_router.get("/fetch/{id}", response_model=Todo)
async def retrieve_event(id: PydanticObjectId, request: Request) -> Todo:
    task = await todo_database.get(id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task with supplied ID does not exist"
        )
    return templates.TemplateResponse("todo.html",
                                      {
                                          "request": request,
                                          "task": task
                                      })


@todo_router.get("/update_todo/{id}", response_model=Todo)
async def update_task(id: PydanticObjectId, request: Request) -> Todo:
    task = await todo_database.get(id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task with supplied ID does not exist"
        )
    return templates.TemplateResponse("update_todo.html",
                                      {
                                          "request": request,
                                          "task": task
                                      })

# @todo_router.put("/update/{id}", response_model=Todo)


@todo_router.post("/update/{id}", response_model=Todo)
async def update_todo(id: PydanticObjectId, body: Todo = Depends(Todo.as_form),) -> Todo:
    req = {k: v for k, v in body.dict().items() if v is not None}
    updated_task = await todo_database.update(id, req)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID does not exist"
        )
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

# @todo_router.delete("/delete/{id}")


@todo_router.get("/delete/{id}")
async def delete_todo(id: PydanticObjectId) -> dict:
    todo = await todo_database.delete(id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID does not exist"
        )

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
