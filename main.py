import fastapi, dataclasses, datetime
from typing import Annotated, Optional

app = fastapi.FastAPI()

database = {}

def generate_new_request_id() -> int:
    request_id = 0

    while request_id in database:
        request_id += 1

    return request_id

@dataclasses.dataclass
class Request:
    number: int = dataclasses.field(default_factory=generate_new_request_id, init=False)
    date: datetime.datetime = dataclasses.field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), init=False)
    state: str = dataclasses.field(default_factory=lambda: "new", init=False)

    type: str
    model: str
    description: str
    fio: str
    phone: str

def add(type: str, model: str, description: str, fio: str, phone: str) -> Optional[dict]:
    request = Request(type, model, description, fio, phone)

    database[request.number] = request

    return dataclasses.asdict(request)

@app.get("/")
def _index() -> fastapi.responses.FileResponse:
    return fastapi.responses.FileResponse("html/index.html")

@app.get("/add")
def _add() -> fastapi.responses.FileResponse:
    return fastapi.responses.FileResponse("html/add.html")

@app.get("/list")
def _list() -> fastapi.responses.HTMLResponse:
    return fastapi.responses.HTMLResponse(f"""
                                          <!DOCTYPE html>
                                          <html lang="ru">
                                          <head>
                                              <meta charset="UTF-8">
                                              <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                              <title>Список заявок | Учет заявок на ремонт оргтехники</title>
                                          </head>
                                          <body>
                                              <a href="/">На главную</a>
  
                                              <h1>Список заявок</h1>
                                              <table>
                                                <tr>
                                                    <th></th>
                                                    <th></th>
                                                    <th></th>
                                                    <th></th>
                                                    <th></th>
                                                    <th></th>
                                                </tr>
                                              </table>
                                          </body>
                                          </html>
                                          """)

@app.post("/pseudo-api/add", response_model=None)
def api_add(type: Annotated[str, fastapi.Form()], model: Annotated[str, fastapi.Form()], description: Annotated[str, fastapi.Form()],
            fio:  Annotated[str, fastapi.Form()], phone: Annotated[str, fastapi.Form()]) -> fastapi.responses.FileResponse | fastapi.responses.HTMLResponse:
    request = add(type, model, description, fio, phone)

    if request is None:
        return fastapi.responses.FileResponse("html/add-fail.html")

    return fastapi.responses.HTMLResponse(f"""
                                          <!DOCTYPE html>
                                          <html lang="ru">
                                          <head>
                                              <meta charset="UTF-8">
                                              <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                              <title>Добавить заявку | Учет заявок на ремонт оргтехники</title>
                                          </head>
                                          <body>
                                              <a href="/">На главную</a>
                                              <a href="/add">Добавить заявку</a>
  
                                              <h1>Ваша заявка была успешно создана.</h1>
                                              Номер вашей заявки: {request["number"]}
                                          </body>
                                          </html>
                                          """)
