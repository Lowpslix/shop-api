from typing import List, Optional

from beanie import PydanticObjectId, WriteRules
from fastapi import APIRouter, Depends, HTTPException, status

from server.models.order import Order, OrderItem
from server.models.product import Product
from server.models.user import CartItem, User
from server.routes.auth import get_current_active_user

# Router
router = APIRouter()


@router.get(
    "/", response_description="Home Page Get Products", status_code=status.HTTP_200_OK
)
async def home() -> List[Product]:
    return await Product.find_all().to_list()


@router.get("/product/{id}", response_description="Get Product By id")
async def get_product(id: PydanticObjectId) -> Product:
    product = await Product.find_one(Product.id == id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id: {id} was not found",
        )

    return product


@router.get("/cart", response_description="A user's cart")
async def get_cart(user: User = Depends(get_current_active_user)) -> List:
    product_ids = [item.prodId for item in user.cart]
    products = await Product.find({"_id": {"$in": product_ids}}).to_list()

    cart = []
    for index, product in enumerate(products):
        cart.append({"product": product, "quantity": user.cart[index].quantity})

    return cart


@router.post("/cart/{id}", response_description="Add product to cart")
async def add_to_cart(
    id: PydanticObjectId, user: User = Depends(get_current_active_user)
) -> dict:
    product = await Product.get(id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} was not found!",
        )

    save = -1
    for index, item in enumerate(user.cart):
        if item.prodId == id:
            save = index
            break

    if save != -1:
        user.cart[save].quantity += 1
    else:
        user.cart.append(CartItem(prodId=id, quantity=1))

    await user.save()

    return {"msg": "Product was added to cart"}


@router.post("/cart-delete-item/{id}")
async def delete_from_cart(
    id: PydanticObjectId, user: User = Depends(get_current_active_user)
) -> dict:
    product = await Product.get(id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} doesn't exist",
        )

    save = None
    for index, item in enumerate(user.cart):
        if item.prodId == id:
            save = user.cart[-1]
            user.cart[-1] = item
            user.cart[index] = save
            user.cart.pop()
            break

    await user.save()

    return {"msg": "Product removed from cart"}


@router.post("/order", response_description="Create an order")
async def create_order(user: User = Depends(get_current_active_user)) -> dict:
    product_ids = [item.prodId for item in user.cart]
    products = await Product.find({"_id": {"$in": product_ids}}).to_list()

    cart = []
    for index, product in enumerate(products):
        cart.append(OrderItem(product=product, quantity=user.cart[index].quantity))

    order = Order(products=cart, user=user)

    await order.save(link_rule=WriteRules.WRITE)

    user.cart = []
    await user.save()

    return {"msg": "Order created successfully"}


@router.get("/orders")
async def get_order(user: User = Depends(get_current_active_user)) -> List:
    records = await Order.find(Order.user.id == user.id).to_list()

    orders = []
    for order in records:
        orders.append(
            {"id": order.id, "products": [product for product in order.products]}
        )

    return orders
