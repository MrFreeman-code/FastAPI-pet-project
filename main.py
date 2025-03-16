

def main():
    import uvicorn
    from api.app import app, args

    uvicorn.run(app, **args)


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

if __name__ == "__main__":
    main()

# Аренда облачного сервиса: https://selectel.ru/services/cloud/servers/?section=about&utm_source=youtube.com&utm_medium=referral&utm_campaign=help_cloud_sharedline_13022024_shumeiko_paid