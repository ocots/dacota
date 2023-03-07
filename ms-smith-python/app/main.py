import pathlib
from functools import lru_cache

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

from .smith.src.smith.ternaryDiagram import ternaryDiagram


# This class encapsulates the settings for the application. The default value of debug is False. The Config class is used to specify the location of the .env file, which is used to load the environment variables, and then modifie the default values of the settings.
class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False
    app_auth_token: str
    app_auth_token_prof: str = None
    skip_auth: bool = False

    class Config:
        env_file = ".env"


# The lru_cache decorator is used to cache the result of the function. This is done to avoid reading the .env file every time the function is called. The cached result is returned instead. This means that this function will only be called once, and the result will be cached for subsequent calls.
@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
DEBUG = settings.debug
BASE_DIR = pathlib.Path(__file__).parent

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def home_view(request: Request, settings: Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/")
def home_view():
    return {"Hello": "World"}


@app.post("/parameters-echo/")
async def parameters_echo_view(
    request: Request, settings: Settings = Depends(get_settings)
):
    if not settings.echo_active:
        raise HTTPException(status_code=400, detail="Invalid endpoint")
    json = await request.json()
    return json


def verify_parameters(parameters):
    c1 = parameters.get("c1")
    c2 = parameters.get("c2")
    c3 = parameters.get("c3")
    a = parameters.get("a")
    alpha = parameters.get("alpha")
    if not c1 or not c2 or not c3 or not a or not alpha:
        return False
    if len(c1) != 3 or len(c2) != 3 or len(c3) != 3:
        return False
    if len(a) != 3 or len(a[0]) != 3 or len(a[1]) != 3 or len(a[2]) != 3:
        return False
    if (
        len(alpha) != 3
        or len(alpha[0]) != 3
        or len(alpha[1]) != 3
        or len(alpha[2]) != 3
    ):
        return False
    # Check type of parameters
    if (
        not isinstance(c1, list)
        or not isinstance(c2, list)
        or not isinstance(c3, list)
    ):
        return False
    if (
        not isinstance(a, list)
        or not isinstance(a[0], list)
        or not isinstance(a[1], list)
        or not isinstance(a[2], list)
    ):
        return False
    if (
        not isinstance(alpha, list)
        or not isinstance(alpha[0], list)
        or not isinstance(alpha[1], list)
        or not isinstance(alpha[2], list)
    ):
        return False
    # Check if parameters are float
    for i in range(3):
        if (
            (type(c1[i]) != float and type(c1[i]) != int)
            or (type(c2[i]) != float and type(c2[i]) != int)
            or (type(c3[i]) != float and type(c3[i]) != int)
        ):
            return False
        for j in range(3):
            if (type(a[i][j]) != float and type(a[i][j]) != int) or (
                type(alpha[i][j]) != float and type(alpha[i][j]) != int
            ):
                return False

        # if (
        #     not isinstance(c1[i], float)
        #     or not isinstance(c2[i], float)
        #     or not isinstance(c3[i], float)
        # ):
        #     return False
        # for j in range(3):
        #     if not isinstance(a[i][j], float) or not isinstance(alpha[i][j], float):
        #         return False
    return True


def verify_auth(
    authorization=Header(None), setting: Settings = Depends(get_settings)
):
    if setting.debug and setting.skip_auth:
        return
    if authorization is None:
        raise HTTPException(
            status_code=401, detail="Missing authorization header"
        )
    label, token = authorization.split(" ")
    if token != setting.app_auth_token:
        raise HTTPException(
            status_code=401, detail="Invalid authorization token"
        )


@app.post("/ternary-diagram/")
async def ternary_diagram_view(
    request: Request,
    authorization=Header(None),
    settings: Settings = Depends(get_settings),
):
    verify_auth(authorization, settings)
    parameters = await request.json()
    KEYS = ["c1", "c2", "c3", "a", "alpha"]
    if not all(key in parameters for key in KEYS):
        raise HTTPException(
            status_code=400, detail="Missing one or more parameters"
        )
    if not verify_parameters(parameters):
        raise HTTPException(status_code=400, detail="Invalid parameters")
    diagram = ternaryDiagram(parameters)
    return diagram
