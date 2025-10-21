from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from main import evaluate_expression
import io
import sys

app = FastAPI()


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/run")
async def run_code(data: dict):
    x = data.get("x")
    y = data.get("y")

    
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

    return JSONResponse({"output": output})
