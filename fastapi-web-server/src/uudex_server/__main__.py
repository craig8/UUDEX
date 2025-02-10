if __name__ == '__main__':
    import uvicorn

    uvicorn.run(reload=True,
                app="uudex_server.main:app",
                port=8001,
                root_path="/api",
                env_file=settings_file.as_posix())
