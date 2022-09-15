from fastapi import FastAPI
from database import engine, Base
from routers import authentication, blog, user



myApp = FastAPI()

### to run the server ###
# uvicorn yourFileName:yourAppInstance --reload

### to run the server in debug mode ###
# from the leftside of vscode click run and debug and select fastAPI

### to open app docs ###
# localhost:8000/docs
# or
# localhost:8000/redoc

Base.metadata.create_all(bind=engine)

myApp.include_router(blog.router)
myApp.include_router(user.router)
myApp.include_router(authentication.router)










### to run the app on different port ###

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(myApp, host="127.0.0.1", port=9000)
