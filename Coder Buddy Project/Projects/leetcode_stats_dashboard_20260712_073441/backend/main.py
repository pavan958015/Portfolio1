import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import httpx

# --- Setup Application ---
app = FastAPI(title="LeetCode Stats Proxy")

class StatsRequest(BaseModel):
    username: str

# --- LeetCode API Integration ---
async def fetch_leetcode_data(username: str) -> dict:
    url = "https://leetcode.com/graphql/"
    query = """
    query userProblemsSolved($username: String!) {
      allQuestionsCount {
        difficulty
        count
      }
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          ranking
          reputation
        }
      }
    }
    """
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url, 
                json={"query": query, "variables": {"username": username}}, 
                headers=headers,
                timeout=10
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=502, detail="Failed to connect to LeetCode GraphQL API.")
            
            payload = response.json()
            if "errors" in payload:
                raise HTTPException(status_code=404, detail="User not found on LeetCode.")
                
            data = payload.get("data", {})
            if not data or not data.get("matchedUser"):
                raise HTTPException(status_code=404, detail="User profile not found or is private.")
                
            return data
            
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Request to LeetCode failed: {str(e)}")

# --- Endpoints ---
@app.post("/api/stats")
async def get_stats(request: StatsRequest):
    username = request.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username is required.")
        
    raw_data = await fetch_leetcode_data(username)
    
    # Parse LeetCode GraphQL response
    all_questions = {q["difficulty"]: q["count"] for q in raw_data["allQuestionsCount"]}
    
    matched_user = raw_data["matchedUser"]
    submit_stats = matched_user["submitStats"]["acSubmissionNum"]
    user_solved = {s["difficulty"]: s["count"] for s in submit_stats}
    
    ranking = matched_user["profile"]["ranking"]
    reputation = matched_user["profile"]["reputation"]
    
    return {
        "username": username,
        "ranking": ranking,
        "reputation": reputation,
        "stats": {
            "all": {
                "solved": user_solved.get("All", 0),
                "total": all_questions.get("All", 0)
            },
            "easy": {
                "solved": user_solved.get("Easy", 0),
                "total": all_questions.get("Easy", 0)
            },
            "medium": {
                "solved": user_solved.get("Medium", 0),
                "total": all_questions.get("Medium", 0)
            },
            "hard": {
                "solved": user_solved.get("Hard", 0),
                "total": all_questions.get("Hard", 0)
            }
        }
    }

# --- Serve Static Frontend Files ---
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
app.mount("/frontend", StaticFiles(directory=frontend_dir, html=True), name="frontend")

@app.get("/")
def read_root():
    return RedirectResponse(url="/frontend/")