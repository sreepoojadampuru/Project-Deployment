from django.shortcuts import render
import subprocess
import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def base(request):
    return render(request, 'pro/base.html')


def profile(request):
    return render(request, 'pro/profile.html')


def login(request):
    return render(request, 'pro/login.html')


def logout(request):
    return render(request, 'pro/logout.html')


def reg(request):
    return render(request, 'pro/reg.html')


def settings(request):
    return render(request, 'pro/settings.html')


def he(request):
    return render(request, 'pro/he.html')


def editor(request):
    return render(request, 'pro/editor.html')


def about(request):
    return render(request, 'pro/about.html')


def notes(request):
    return render(request, 'pro/notes.html')


def success(request):
    return render(request, 'pro/success.html')


@csrf_exempt
def run_java_code(request):
    if request.method == 'POST':
        # Get the Java code from the request body
        java_code = request.POST.get('code')

        if not java_code:
            return JsonResponse({"error": "No code provided"}, status=400)

        # Save the Java code to a temporary .java file
        file_path = 'temp.java'
        with open(file_path, 'w') as file:
            file.write(java_code)

        # Compile the Java code using subprocess
        try:
            compile_command = ['javac', file_path]
            compile_process = subprocess.run(compile_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # If compilation succeeds, run the Java program
            run_command = ['java', 'temp']
            run_process = subprocess.run(run_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Get the output of the Java program
            output = run_process.stdout.decode('utf-8')
            return JsonResponse({"output": output})

        except subprocess.CalledProcessError as e:
            # If there is an error during compilation or execution
            error_message = e.stderr.decode('utf-8') if e.stderr else e.stdout.decode('utf-8')
            return JsonResponse({"error": error_message}, status=500)

        finally:
            # Clean up by deleting the temporary files
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists('temp.class'):
                os.remove('temp.class')

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt

def execute_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            language = data.get('language')
            code = data.get('code')

            # Handle Python code execution
            if language == 'python':
                result = execute_python_code(code)
            # Handle Java code execution
            elif language == 'java':
                result = run_java_code(code)
            # Handle JavaScript code execution
            elif language == 'javascript':
                result = execute_javascript_code(code)
            elif language == 'c':
                result = "C execution is not implemented yet."
            elif language == 'cpp':
                result = "C++ execution is not implemented yet."
            else:
                result = "Language not supported."

            return JsonResponse({'output': result})

        except Exception as e:
            return JsonResponse({'output': 'Error: ' + str(e)})

    return JsonResponse({'output': 'Invalid request method.'})

def execute_javascript_code(code):
    try:
        # Save the JavaScript code to a temporary .js file
        js_file_path = 'TempJavaFile.js'
        with open(js_file_path, 'w') as js_file:
            js_file.write(code)

        # Execute the JavaScript code using Node.js
        run_process = subprocess.run(['node', js_file_path], capture_output=True, text=True)

        # Return the output or error from running the JavaScript code
        if run_process.returncode == 0:
            return run_process.stdout  # Return the successful output
        else:
            return run_process.stderr  # Return the error if execution fails

    except Exception as e:
        return str(e)

def execute_python_code(code):
    try:
        # Run the code in a subprocess (safe environment)
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True
        )
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)









