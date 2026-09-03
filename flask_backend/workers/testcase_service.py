from workers.redis_client import get_redis


def get_test_cases(problem_id):
    redis_client = get_redis()
    count = int(redis_client.get(f"problem_{problem_id}/count"))
    test_cases = []

    for index in range(1, count + 1):
        test_cases.append(
            {
                "input": redis_client.get(f"problem_{problem_id}/input_{index}"),
                "expected_output": redis_client.get(
                    f"problem_{problem_id}/output_{index}"
                ),
            }
        )

    return test_cases


def get_system_solution(problem_id):
    return get_redis().get(f"problem_{problem_id}/solution")
