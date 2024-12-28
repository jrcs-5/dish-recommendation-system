from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from llm import LLM
import os

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

llm = LLM()

@app.get("/", response_class=HTMLResponse)
async def get_welcome_page(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "llm": llm})



@app.post("/chat/", response_class=PlainTextResponse)
async def chat(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message")
        portions = body.get("portions", 1)
        response_type = body.get("type") 
        if not user_message:
            raise HTTPException(status_code=400, detail="El campo 'message' es obligatorio.")
        if response_type == "recetario":
            #print("Recetario")
            response = llm.generate_response(user_message, portions)
        elif response_type == "libre":
            #print("Libre")
            response = llm.generate_free_response(user_message, portions)
        else:
            raise HTTPException(status_code=400, detail="No indico el tipo de receta que desea obtener.")
        
        return PlainTextResponse(response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/manage-recipes", response_class=HTMLResponse)
async def manage_recipes_page(request: Request):
    return templates.TemplateResponse("manage-recipes.html", {"request": request})


@app.get("/dishes", response_class=JSONResponse)
async def get_dishes():
    try:
        dishes_path = os.path.join("static", "dishes.txt")
        if not os.path.exists(dishes_path):
            raise HTTPException(status_code=404, detail="El recetario no se encuentra.")
        
        with open(dishes_path, "r", encoding="utf-8") as file:
            dishes_list = file.read().splitlines()
        
        if not dishes_list:
            return JSONResponse({"dishes": []})
        
        return JSONResponse({"dishes": dishes_list})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))