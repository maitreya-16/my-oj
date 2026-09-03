import base64
import logging

from workers.docker_runner import (
    create_working_directory,
    write_content_to_file,
    compile_code,
    create_and_start_container,
    run_single_test_case,
    cleanup,
)
from workers.language_config import get_language_config
from workers.testcase_service import get_system_solution, get_test_cases


def decode(encoded_value):
    return base64.b64decode(encoded_value, validate=True).decode("utf-8")


def run_code(submission_id, problem_id, code, language, inputData=""):
    container = None
    try:
        config, error = get_language_config(language)
        if error:
            return error

        work_dir = create_working_directory(submission_id)
        write_content_to_file(work_dir, decode(code), f"Main{config['extension']}")
        write_content_to_file(work_dir, decode(inputData), "input.txt")

        container = create_and_start_container(config, submission_id)
        compile_result = compile_code(container, config)
        if compile_result:
            return compile_result

        return run_single_test_case(container, config)
    except Exception as error:
        logging.error("An error occurred during execution: %s", error)
        return {"status": "failed", "message": str(error)}
    finally:
        cleanup(submission_id, container)


def run_system_code(submission_id, problem_id, inputData=""):
    container = None
    try:
        config, error = get_language_config("cpp")
        if error:
            return error

        solution = get_system_solution(problem_id)
        if not solution:
            return {"status": "failed", "message": "Solution code not found"}

        work_dir = create_working_directory(submission_id)
        write_content_to_file(work_dir, decode(solution), f"Main{config['extension']}")
        write_content_to_file(work_dir, decode(inputData), "input.txt")

        container = create_and_start_container(config, submission_id)
        compile_result = compile_code(container, config)
        if compile_result:
            return compile_result

        return run_single_test_case(container, config)
    except Exception as error:
        logging.error("An error occurred during system execution: %s", error)
        return {"status": "failed", "message": str(error)}
    finally:
        cleanup(submission_id, container)


def submit(submission_id, problem_id, code, language):
    container = None
    try:
        config, error = get_language_config(language)
        if error:
            return error

        work_dir = create_working_directory(submission_id)
        write_content_to_file(work_dir, decode(code), f"Main{config['extension']}")

        container = create_and_start_container(config, submission_id)
        compile_result = compile_code(container, config)
        if compile_result:
            return compile_result

        test_cases = get_test_cases(problem_id)
        total_test_cases = len(test_cases)

        for index, test_case in enumerate(test_cases, start=1):
            write_content_to_file(work_dir, decode(test_case["input"]), "input.txt")
            run_result = run_single_test_case(container, config)
            if run_result["status"] != "success":
                return {
                    "status": run_result["status"],
                    "message": run_result["message"],
                    "failed_test_case": index,
                    "total_test_case": total_test_cases,
                    "score": 0,
                }

            user_output = run_result["user_output"].strip()
            expected_output = decode(test_case["expected_output"]).strip()
            if user_output != expected_output:
                return {
                    "status": "wrong",
                    "message": "Failed Testcase",
                    "failed_test_case": index,
                    "total_test_case": total_test_cases,
                    "score": (index - 1) * 10,
                }

        return {
            "status": "accepted",
            "message": None,
            "failed_test_case": 0,
            "total_test_case": total_test_cases,
            "score": total_test_cases * 100,
        }
    except Exception as error:
        logging.error("An error occurred during submission evaluation: %s", error)
        return {"status": "failed", "message": str(error)}
    finally:
        cleanup(submission_id, container)
