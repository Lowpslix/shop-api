from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from server.models.product import Product, UpdateProduct

router = APIRouter()


@router.get(
    "/products", response_description="Get products", status_code=status.HTTP_200_OK
)
async def get_products() -> List[Product]:
    products = await Product.find_all().to_list()
    return products


@router.post(
    "/add-product",
    response_description="Add new product",
    status_code=status.HTTP_201_CREATED,
)
async def add_product(product: Product) -> dict:
    await product.create()
    return {"msg": "Product added successfully"}


@router.put("/edit-product/{id}", response_description="Edit a product")
async def edit_product(id: PydanticObjectId, product: UpdateProduct) -> Product:
    update_query = {"$set": {k: v for k, v in product.dict().items() if v is not None}}
    prod = await Product.get(id)

    if not prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id: {id} not found",
        )

    await prod.update(update_query)
    return prod


@router.delete("/delete-product/{id}", response_description="Product is deleted")
async def delete_product(id: PydanticObjectId):
    product = await Product.get(id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id: {id} was not found",
        )

    await product.delete()
    return {"msg": "product deleted!"}
