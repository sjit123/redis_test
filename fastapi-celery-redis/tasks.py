from celery import Celery
import time
import random

 # Configure Celery.  'redis://localhost:6379/0' is the default Redis URL.
app = Celery('my_tasks', broker='redis://localhost:6379/0' , backend='redis://localhost:6379/0')

@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def long_running_task(self, a, b):
    """
    A simulated long-running task.  It takes two numbers,
    waits for a random amount of time (to simulate work),
    and then returns their sum.  It demonstrates retries.
    """
    try:
        delay = random.randint(1, 10)  # Simulate varying task duration
        print(f"Task {self.request.id}: Starting.  Will sleep for {delay} seconds...")
        time.sleep(delay)

        if random.random() < 0.2:  # Simulate a 20% chance of failure
            raise ValueError("Task failed randomly!")

        result = a + b
        print(f"Task {self.request.id}: Finished. Result: {result}")
        return result
    except Exception as exc:
        print(f"Task {self.request.id}: Failed. Retrying...")
        raise self.retry(exc=exc)

@app.task
def quick_task(text):
    print(f"Quick task received text: {text}")
    return f"Processed: {text}"