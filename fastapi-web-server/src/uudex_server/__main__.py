if __name__ == '__main__':
    import os

    import uvicorn

    uvicorn.run(reload=True, app="uudex_server.main:app", port=8001, root_path="/api", env_file=".env")
