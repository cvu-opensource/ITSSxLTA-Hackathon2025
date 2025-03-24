from fastapi import FastAPI

# Initialise app
app = FastAPI()


@app.get('/healthz')
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

@app.get('/get_planning_recommendations')
def get_planning_recommendations():
    return