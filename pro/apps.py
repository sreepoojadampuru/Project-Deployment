from django.apps import AppConfig
from flask import Flask, request, jsonify
import subprocess
import uuid
import os

class ProConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pro'


app = Flask(__name__)

# Directory to store temporary files
TEMP_DIR = "/tmp/code-execution"

# Ensure TEMP_DIR exists
os.makedirs(TEMP_DIR, exist_ok=True)

# Language-specific Docker images
DOCKER_IMAGES = {
    "python": "python:3.8-slim",
    "java": "openjdk:11-jdk-slim",
    "c": "gcc:latest",
    "cpp": "gcc:latest"
}


# Run code in Docker container
def run_code_in_docker(language, code):
    filename = f"{uuid.uuid4()}"
    file_path = os.path.join(TEMP_DIR, filename)
    output = ""
    try:
        # Determine file extension and docker command
        if language == "python":
            file_path += ".py"
            with open(file_path, "w") as f:
                f.write(code)
            command = f"docker run --rm -v {TEMP_DIR}:/code {DOCKER_IMAGES[language]} python /code/{filename}.py"

        elif language == "java":
            file_path += ".java"
            with open(file_path, "w") as f:
                f.write(code)
            command = f"docker run --rm -v {TEMP_DIR}:/code {DOCKER_IMAGES[language]} bash -c 'javac /code/{filename}.java && java -cp /code {filename}'"

        elif language in ["c", "cpp"]:
            extension = ".c" if language == "c" else ".cpp"
            file_path += extension
            with open(file_path, "w") as f:
                f.write(code)
            command = f"docker run --rm -v {TEMP_DIR}:/code {DOCKER_IMAGES[language]} bash -c 'gcc /code/{filename}{extension} -o /code/{filename} && /code/{filename}'"

        # Run the command and capture output
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode() + result.stderr.decode()

    except Exception as e:
        output = f"Error: {str(e)}"

    finally:
        # Cleanup: remove the file after execution
        if os.path.exists(file_path):
            os.remove(file_path)

    return output


# Flask route for executing code
@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    language = data.get("language")
    code = data.get("code")

    if language not in DOCKER_IMAGES:
        return jsonify({"error": "Unsupported language"}), 400

    # Run code and get output
    output = run_code_in_docker(language, code)
    return jsonify({"output": output})


if __name__ == '__main__':
    app.run(debug=True)
