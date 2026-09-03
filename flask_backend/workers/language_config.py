LANGUAGE_CONFIG = {
    "cpp": {
        "extension": ".cpp",
        "image": "gcc:latest",
        "compile_cmd": "g++ Main.cpp -o exec",
        "run_command": "./exec",
        "timeout": 3,
        "memory_limit": "256m",
    },
    "python": {
        "extension": ".py",
        "image": "python:3.9-alpine",
        "run_command": "python Main.py",
        "timeout": 5,
        "memory_limit": "256m",
    },
    "java": {
        "extension": ".java",
        "image": "eclipse-temurin:21-jdk",
        "compile_cmd": "javac Main.java",
        "run_command": "java Main",
        "timeout": 5,
        "memory_limit": "256m",
    },
}


def get_language_config(language):
    if language not in LANGUAGE_CONFIG:
        return None, {
            "status": "failed",
            "message": "Unsupported Programming Language",
        }

    return LANGUAGE_CONFIG[language], None
