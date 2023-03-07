from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/products', tags=['Products'])

# Mensajes predeterminados
NO_EXISTE_PRODUCTO = 'No existe un poroducto con ese ID'

products_list = ['Producto 1','Producto 2','Producto 3','Producto 5','Producto 4']

@router.get('/')
async def products():
    return products_list

@router.get('/{id}')
async def products(id:int):
    try:
        return products_list[id]
    except:
        raise HTTPException(status_code=404, detail=NO_EXISTE_PRODUCTO)