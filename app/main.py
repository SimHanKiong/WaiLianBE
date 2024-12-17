from fastapi import FastAPI
from sqlalchemy import text

from app.api.deps import SessionDep

app = FastAPI()


@app.get("/")
async def root(session: SessionDep):
    result = session.execute(text("SELECT 'hello' AS message"))  # Fixed query
    message = result.scalar()  # Fetch the result (scalar for single value)
    return {"message": message}
