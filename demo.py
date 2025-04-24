# from supabase import create_client , Client

# SUPABASE_URL="https://ncctimunmjorihqnfdqn.supabase.co"
# SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5jY3RpbXVubWpvcmlocW5mZHFuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTUxMDcxOSwiZXhwIjoyMDYxMDg2NzE5fQ.vWUWotubrOytbwtFqjhxOyPBuNDOk5NDtPgNp6v0nMo"

# supabase:Client = create_client(SUPABASE_URL , SUPABASE_KEY)

#insert a new row in table
# new_row = {'Lang':'اللهجة السعودية'}
# supabase.table('Languages').insert(new_row).execute()

# #updata row
# update_row = {'Lang':'اللهجة السورية'}
# supabase.table('Languages').update(update_row).eq('id', 2).execute()

# result = supabase.table('Languages').select('*').execute()

# # result.data هي قائمة القواميس
# langs = [row['Lang'] for row in result.data]
# print(langs)




from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from typing import List
from dotenv import load_dotenv
import os
import uvicorn



load_dotenv(dotenv_path=".env.local")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI instance
app = FastAPI()

# Pydantic model for Language
class Language(BaseModel):
    lang: str

# POST endpoint to insert a new language
@app.post("/addLanguage", status_code=201)
async def create_language(new_language: Language):
    try:
        # Insert new row into 'Languages' table
        new_row = {'Lang': new_language.lang}
        supabase.table('Languages').insert(new_row).execute()
        
        return {"message": "Language added successfully", "data": new_row}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# GET endpoint to retrieve all languages as a list
@app.get("/getLanguages")
async def get_languages():
    try:
        # Fetch all languages from the 'Languages' table
        result = supabase.table('Languages').select('Lang').execute()
                
        return [row['Lang'] for row in result.data]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# To run the server, use the command: uvicorn main:app --reload

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)