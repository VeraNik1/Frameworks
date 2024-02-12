from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import starlette.status as status
from models import User, Product, Order, UserIn, ProductIn, OrderIn
from dbase import database, users, products, orders
from typing import List
from hashlib import sha256


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.api_route("/", methods=['GET', 'HEAD'], response_class=RedirectResponse)
async def main_page():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)
#--------------------------------------------------------------------------------------------------------
# CRUD операции "Чтение всех"
#--------------------------------------------------------------------------------------------------------

# Вывод всех пользователей в БД
@app.api_route("/user/", methods=['GET', 'HEAD'], response_model=List[User])
async def get_all_users():
    return await database.fetch_all(users.select())

# Вывод всех товаров в БД
@app.api_route("/product/", methods=['GET', 'HEAD'], response_model=List[Product])
async def get_all_products():
    return await database.fetch_all(products.select())

# Вывод всех заказов в БД
@app.api_route("/order/", methods=['GET', 'HEAD'], response_model=List[Order])
async def get_all_orders():
    return await database.fetch_all(orders.select())

#--------------------------------------------------------------------------------------------------------
# CRUD операции "Чтение одного"
#--------------------------------------------------------------------------------------------------------

# Вывод данных о пользователе по id
@app.api_route("/user/{user_id}", methods=['GET', 'HEAD'], response_model=User)
async def get_user(user_id: int):
    user = await database.fetch_one(users.select().where(users.c.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{user_id}' not found")
    return user

# Вывод данных о товаре по id
@app.api_route("/product/{product_id}", methods=['GET', 'HEAD'], response_model=Product)
async def get_product(product_id: int):
    product = await database.fetch_one(products.select().where(products.c.id == product_id))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id '{product_id}' not found")
    return product

# Вывод данных о заказе по id
@app.api_route("/order/{order_id}", methods=['GET', 'HEAD'], response_model=Order)
async def get_order(order_id: int):
    order = await database.fetch_one(orders.select().where(orders.c.id == order_id))
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id '{order_id}' not found")
    return order

#--------------------------------------------------------------------------------------------------------
# CRUD операции "Запись"
#--------------------------------------------------------------------------------------------------------

# Создать нового пользователя в БД
@app.post("/user/", response_model=User)
async def create_user(user: UserIn):
    user.password = sha256(user.password.encode("utf-8")).hexdigest()
    query = users.insert().values(
        **user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}

# Создать новый товар в БД
@app.post("/product/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(
        **product.model_dump())
    last_record_id = await database.execute(query)
    return {**product.model_dump(), "id": last_record_id}

# Создать новый заказ
@app.post("/order/", response_model=Order)
async def create_order(order: OrderIn):
    user = await database.fetch_one(users.select().where(users.c.id == order.user_id))
    product = await database.fetch_one(products.select().where(products.c.id == order.product_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id '{order.user_id}' not exist")
    if not product:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product with id '{order.product_id}' not exist")
    query = orders.insert().values(
        **order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}

#--------------------------------------------------------------------------------------------------------
# CRUD операции для "Изменение"
#--------------------------------------------------------------------------------------------------------

# Обновить информацию о пользователе в БД(по id)
@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    user = await database.fetch_one(users.select().where(users.c.id == user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{user_id}' not found")
    new_user.password = sha256(new_user.password.encode("utf-8")).hexdigest()
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}

# Обновить информацию о товаре в БД(по id)
@app.put("/product/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    product = await database.fetch_one(products.select().where(products.c.id == product_id))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id '{product_id}' not found")
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}

# Обновить информацию о заказе в БД(по id)
@app.put("/order/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    order = await database.fetch_one(orders.select().where(orders.c.id == order_id))
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id '{order_id}' not found")
    user = await database.fetch_one(users.select().where(users.c.id == order.user_id))
    product = await database.fetch_one(products.select().where(products.c.id == order.product_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id '{order.user_id}' not exist")
    if not product:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product with id '{order.product_id}' not exist")
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}
    
#--------------------------------------------------------------------------------------------------------
# CRUD операции "Удаление"
#--------------------------------------------------------------------------------------------------------

# Удалить пользователя из БД(по id)
@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    # TODO: add 404 if trying to delete not existing element
    user_orders = await database.fetch_one(orders.select().where(orders.c.user_id == user_id))
    # проверка на наличие у пользователя действующих заказов
    if user_orders:
        for order in user_orders:
            if order.status not in ['выполнен','отменен']:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User has Orders, delete Orders first")
    await database.execute(users.delete().where(users.c.id == user_id))
    return {"message": "User deleted"}

# Удалить пользователя из БД(по id)
@app.delete("/product/{product_id}")
async def delete_product(product_id: int):
    # TODO: add 404 if trying to delete not existing element
    product_orders = await database.fetch_one(orders.select().where(orders.c.product_id == product_id))
    if product_orders:
        for order in product_orders:
            if order.status not in ['выполнен','отменен']:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"This product included in Orders, delete Orders first")
    await database.execute(products.delete().where(products.c.id == product_id))
    return {"message": "Product deleted"}
    
# Удалить заказ из БД(по id)
@app.delete("/order/{order_id}")
async def delete_order(order_id: int):
    # TODO: add 404 if trying to delete not existing element
    await database.execute(orders.delete().where(orders.c.id == order_id))
    return {"message": "Order deleted"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
