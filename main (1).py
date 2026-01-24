from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/success", response_class=HTMLResponse)
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.post("/web/register")
async def web_register(
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...),
    role: str = Form(...) # 'buyer' or 'seller'
):
    date_now = datetime.now().strftime("%Y-%m-%d")
    
    try:
        if role == "buyer":
            # Match your filename exactly: BuyerLogin.py
            from Buyer_Login import Buyer_Login
            manager = Buyer_Login()
            result = manager.create_buyer_account(name, email, "Web-User", "000", password, date_now)
        else:
            # Match your filename exactly: Seller_Login.py
            from Seller_Login import Seller_Login
            manager = Seller_Login()
            result = manager.create_seller_account(name, "Web Business", "Retail", "000", email, password, "Web", "08:00", 0, 0, date_now, "default.png")
        
        # Check the result from your Backend Classes
        if result == 1:
            print(f"Technical Success: {role} account created for {name}")
            return RedirectResponse(url="/success", status_code=303)
        else:
            return {"status": "error", "message": result}
            
    except Exception as e:
        print(f"Backend Logic Error: {e}")
        return {"status": "error", "message": str(e)}