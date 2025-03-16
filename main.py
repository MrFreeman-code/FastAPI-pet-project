

def main():
    import uvicorn
    from api.app import app, args

    uvicorn.run(app, **args)


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == "__main__":
    main()