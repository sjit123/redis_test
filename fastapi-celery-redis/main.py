from fastapi import FastAPI, HTTPException
from tasks import long_running_task, quick_task

app = FastAPI()

@app.post("/long_task")
async def run_long_task(a: int, b: int):
    """
    Starts the long-running task.
    """
    task = long_running_task.delay(a, b)  # Enqueue the task
    return {"task_id": task.id, "status": "pending"}

@app.post("/quick_task")
async def run_quick_task(text: str):
    task = quick_task.delay(text)
    return {"task_id": task.id, "status": "pending"}

@app.get("/task_status/{task_id}")
async def get_task_status(task_id: str):
     """
     Checks the status of a task.
     """
     task_result = long_running_task.AsyncResult(task_id) #Also works for quick_task.
     if task_result.state == 'PENDING':
         response = {
             'state': task_result.state,
             'status': 'Pending...'
         }
     elif task_result.state != 'FAILURE':
         response = {
             'state': task_result.state,
             'result': task_result.result
         }
         if task_result.state == 'SUCCESS': # remove after testing
           pass
     else:
         # something went wrong in the background job
         response = {
             'state': task_result.state,
             'status': str(task_result.info),  # this is the exception raised
         }
     return response