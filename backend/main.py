
from fastapi import FastAPI
from presentation.book_router import router as book_router
from presentation.auth_router import router as auth_router
from presentation.catalog_router import router as catalog_router
from presentation.article_router import router as article_router
from presentation.stock_router import router as stock_router
from presentation.order_router import router as order_router
from presentation.scan_router import router as scan_router
from presentation.user_router import router as user_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(book_router)
app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(article_router)
app.include_router(stock_router)
app.include_router(order_router)
app.include_router(scan_router)
app.include_router(user_router)