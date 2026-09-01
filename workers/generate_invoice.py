from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.worker_task import worker_task
from conductor.client.configuration.configuration import AuthenticationSettings


CONDUCTOR_SERVER_URL = '<url>'
CONDUCTOR_AUTH_KEY = '<key>'
CONDUCTOR_AUTH_SECRET = '<secret>'


@worker_task(task_definition_name="generate_invoice")
def generate_invoice(orderId: str, finalAmount: float, transactionId: str) -> dict:
    return {
        "invoiceNumber": f"INV-{orderId}",
        "amount": finalAmount,
        "transactionId": transactionId,
    }
    

if __name__ == "__main__":
    api_config = Configuration(
        server_api_url=CONDUCTOR_SERVER_URL,
        authentication_settings=AuthenticationSettings(
            key_id=CONDUCTOR_AUTH_KEY,
            key_secret=CONDUCTOR_AUTH_SECRET
        ),
    )    
    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()
