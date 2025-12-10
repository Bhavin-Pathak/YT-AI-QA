if __name__ == "__main__":
    import uvicorn
    # Run the app from app.main
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
