from celery import Celery
import requests
import os

from workers.submission_runner import (
    run_code as execute_code,
    run_system_code as execute_system_code,
    submit as evaluate_submission,
)


BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:3000')
REDIS_BROKER_URL = os.getenv('REDIS_BROKER_URL', 'redis://redis:6379/0')
REDIS_BACKEND_URL = os.getenv('REDIS_BACKEND_URL', 'redis://redis:6379/0')

app = Celery(    
    'tasks',
    broker=REDIS_BROKER_URL,
    backend=REDIS_BACKEND_URL,
)
app.conf.update(
    broker_heartbeat=10,
    broker_connection_timeout=30,
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

app.conf.result_expires = 3600  # seconds me he.. 1 hour

WEBHOOK_URL_RUN = f'{BACKEND_URL}/webhook/run'
WEBHOOK_URL_SUBMIT = f'{BACKEND_URL}/webhook/submit'
WEBHOOK_URL_SYSTEM = f'{BACKEND_URL}/webhook/system'


def send_webhook_result(url, data):
    """POST result to webhook endpoint."""
    try:
        print(f"[Webhook] Sending to {url}")
        r = requests.post(url, json=data, timeout=10)
        r.raise_for_status()
        print("[Webhook] Sent successfully.")
    except Exception as e:
        print(f"[Webhook] Failed to send: {e}")


# ─── Task: Run System Code ──────────────────────────────────────────────

@app.task(name="tasks.run_code", queue="runQueue")
def run_code(data):
    result = execute_code(
        submission_id=data['submission_id'],
        code=data['code'],
        language=data['language'],
        problem_id=data['problem_id'],
        inputData=data['customTestcase']
    )
    webhook_data = {
        'submission_id': data['submission_id'],
        'status': result.get('status'),
        'message': result.get('message'),
        'expected_output': result.get('expected_output'),
        'user_output':result.get('user_output')
        
    }
    send_webhook_result(WEBHOOK_URL_RUN, webhook_data)
    return result


# ─── Task: Code Submission ──────────────────────────────────────────────

@app.task(name="tasks.submit_code", queue="submitQueue")
def submit_code(data):
    result = evaluate_submission(
        submission_id=data['submission_id'],
        problem_id=data['problem_id'],
        code=data['code'],
        language=data['language'],
    )
    webhook_data = {
        'submission_id':data["submission_id"],
        'status':result.get('status'),
        'message':result.get('message'),
        'failed_test_case':result.get('failed_test_case'),
        'total_test_case':result.get('total_test_case'),
        'score':result.get('score'),
    }
    send_webhook_result(WEBHOOK_URL_SUBMIT, webhook_data)
    return (result)

# ─── Task: Run System Code ──────────────────────────────────────────────

@app.task(name="tasks.run_system_code", queue="runSystemQueue")
def run_system_code(data):

    result = execute_system_code(
        submission_id=data['submission_id'],
        problem_id=data['problem_id'],
        inputData=data.get('customTestcase')
    )
    
    webhook_data = {
        'submission_id': data['submission_id'],
        'status': result.get('status'),
        'message': result.get('message'),
        'user_output':result.get('user_output')
    }
    send_webhook_result(WEBHOOK_URL_SYSTEM, webhook_data)
    return result
