import logging
import os
import shutil
import sys

import docker


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

client = docker.from_env()


def create_working_directory(submission_id):
    work_dir = f"./{submission_id}"
    os.makedirs(work_dir, exist_ok=True)
    return work_dir


def write_content_to_file(work_dir, content, filename):
    file_path = os.path.join(work_dir, filename)
    with open(file_path, "w") as file:
        file.write(content)


def create_and_start_container(config, submission_id):
    container = client.containers.create(
        config["image"],
        mem_limit=config["memory_limit"],
        volumes={
            "submissions": {
                "bind": "/app/submissions",
                "mode": "rw",
            }
        },
        tty=True,
        working_dir=f"/app/submissions/{submission_id}",
        command="sleep infinity",
    )
    container.start()
    return container


def compile_code(container, config):
    if not config.get("compile_cmd"):
        return None

    exit_code, (stdout, stderr) = container.exec_run(
        config["compile_cmd"], demux=True
    )
    stdout = stdout.decode("utf-8") if stdout else ""
    stderr = stderr.decode("utf-8") if stderr else ""

    logging.info("Compilation completed with exit code %s", exit_code)
    if exit_code != 0:
        logging.error("Compilation Error: %s", stderr)
        return {"status": "failed", "message": stderr}

    return None


def run_single_test_case(container, config):
    exit_code, (stdout, stderr) = container.exec_run(
        [
            "sh",
            "-c",
            f"timeout -k 1 {config['timeout']}s {config['run_command']} < input.txt",
        ],
        demux=True,
    )
    stdout = stdout.decode("utf-8") if stdout else ""
    stderr = stderr.decode("utf-8") if stderr else ""

    logging.info("Execution completed with exit code %s", exit_code)
    if exit_code == 124 or exit_code == 143:
        return {"status": "timeout", "message": "Time Limit Exceeded"}
    if exit_code == 137:
        return {"status": "memory_exceeded", "message": "Memory Limit Exceeded"}
    if exit_code != 0:
        return {"status": "runtime_error", "message": stderr}

    return {
        "status": "success",
        "message": "Run Successful",
        "user_output": stdout,
    }


def cleanup(submission_id, container):
    work_dir = f"./{submission_id}"
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
        logging.info("Cleaned up submission directory: %s", work_dir)

    if container:
        container.remove(force=True)
        logging.info("Stopped and removed Docker container")
