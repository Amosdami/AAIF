import sqlite3
import requests
from fastapi import FastAPI, Body

app = FastAPI()

# Database interaction with Northwind
def query_northwind(query):
    conn = sqlite3.connect('northwind.db')  # Assuming downloaded and placed in the same directory
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Public API Integration (Example: RESTful API)
def call_restful_api(endpoint, params=None):
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # Raise exception for non-200 status codes
    return response.json()

# Basic intent classification (can be replaced with a more robust Langchain integration)
def classify_intent(text):
    intent_mapping = {
        'database': 'database_query',
        'northwind': 'database_query',
        'api': 'api_call',
        'call': 'api_call',
    }
    for keyword, intent in intent_mapping.items():
        if keyword.lower() in text.lower():
            return intent
    return 'unknown'

# FAST API endpoint for handling queries
@app.post("/query")
async def handle_query(query: str = Body(...)):
    intent = classify_intent(query)
    if intent == 'database_query':
        results = query_northwind(query)
        return {"results": results}
    elif intent == 'api_call':
        # Example using RESTful API
        api_url = "https://restful-api.dev/some/endpoint"  # Replace with desired API
        api_response = call_restful_api(api_url)
        return {"api_response": api_response}
    else:
        return {"message": "Intent not recognized"}

# Run the Uvicorn server (for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("langchain_agent:app", host="0.0.0.0", port=8000)
