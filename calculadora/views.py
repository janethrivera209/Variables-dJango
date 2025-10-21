from django.shortcuts import render
from django.http import JsonResponse
from main import evaluate_expression
from django.views.decorators.csrf import csrf_exempt
import io
import sys

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def evaluate(request):
    if request.method == 'POST':
        x = request.POST.get('x')
        y = request.POST.get('y')

        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()

        try:
            user_code = (
                f"x = {x}\n"
                f"y = {y}\n"
                f"z = x * y + 10\n"
                f"print(z)\n"
                f"x = x + 1\n"
                f"print(x)\n"
            )
            evaluate_expression(user_code)
            output = mystdout.getvalue()
        except Exception as e:
            output = f"Error: {e}"
        finally:
            sys.stdout = old_stdout

        return JsonResponse({"output": output})
    return JsonResponse({"error": "Invalid request"})
