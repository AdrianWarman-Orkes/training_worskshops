from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.worker_task import worker_task
from conductor.client.configuration.configuration import AuthenticationSettings
from conductor.client.worker.worker import TaskResult
import os

#auth config
SERVER_URL = '<url>'
KEY = '<key>'   
SECRET = '<secret>'

#simple worker -- name must match task name in workflow
@worker_task(task_definition_name='hello_world')
#TaskResult object allows control over setting task status and attaching logs.
#Doesn't have to be used, can also return a string object
def my_task(name: str) -> TaskResult:
    
    result = TaskResult()

    result.log("task in progress...")

    result.add_output_data("greeting", f"Hello {name}!")

    result.status = "COMPLETED"


    return result


if __name__ == "__main__":
  api_config = Configuration(
     server_api_url=SERVER_URL,
     authentication_settings=AuthenticationSettings(
        key_id=KEY,
        key_secret=SECRET
     ),
  )
  task_handler = TaskHandler(configuration=api_config)
  task_handler.start_processes()
