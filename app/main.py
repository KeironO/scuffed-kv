from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "ScuffedCV"
    admin_email: str = "keirono@github.com"
    db_path: str = 'database.db'

    class Config:
        env_file = ".env"

settings = Settings()
app = FastAPI()

import sqlite3


con = sqlite3.connect(
    os.path.join('db', settings.db_path),
    check_same_thread=False
)
cur = con.cursor()

try:
    cur.execute("CREATE TABLE pair(key TEXT UNIQUE, value TEXT)")
except sqlite3.OperationalError as e:
    pass

class Pair(BaseModel):
    value: str

@app.get("/api/kv/{key}")
async def get_item(key: str):
    res = cur.execute("SELECT * FROM pair WHERE key = '%s'" % (key))
    result = res.fetchone()
    if result == None:
        raise HTTPException(status_code=404, detail="The specified key does not exist.")
    return {"value": result[1]}

@app.head("/api/kv/{key}")
async  def head_item(key: str):
    res = cur.execute("SELECT * FROM pair WHERE key = '%s'" % (key))
    result = res.fetchone()
    if result == None:
        raise HTTPException(status_code=404, detail="The specified key does not exist.")
    return {"message": "The specified key is initialised."}

@app.put("/api/kv/{key}")
async def put_item(key: str, value: Pair):
    cur.execute("INSERT INTO pair VALUES ('%s', '%s')" % (key, value.value))
    con.commit()
    return {key: value}

@app.delete("/api/kv/{key}")
async def delete_item(key):
    res = cur.execute("SELECT * FROM pair WHERE key = '%s'" % (key))
    result = res.fetchone()
    if result == None:
        raise HTTPException(status_code=404, detail="The specified key does not exist.")
    cur.execute("DELETE FROM pair WHERE key = '%s'" % (key))
    con.commit()
    return {"message": "The specified key and its data was successfully deleted."}