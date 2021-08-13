import pydantic
import uvicorn
from fastapi import FastAPI


def get_application() -> FastAPI:
    app = FastAPI()
    return app


app = get_application()


class HealthcheckSchema(pydantic.BaseModel):
    status: str


@app.get("/healthcheck", response_model=HealthcheckSchema, include_in_schema=False)
def healthcheck() -> HealthcheckSchema:
    return HealthcheckSchema(status="ok")


@app.on_event("startup")
def startup_event() -> None:
    pass


@app.on_event("shutdown")
def shutdown_event() -> None:
    pass


if __name__ == "__main__":
    uvicorn.run("talk_to_me.main:app", host="0.0.0.0", port=8080, reload=False)
