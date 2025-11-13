import boto3
from boto3.dynamodb.conditions import Attr

# 1. Crear un recurso de servicio de DynamoDB
# Reemplaza 'us-east-1' con la región que estés utilizando
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# 2. Seleccionar la tabla 'Orders'
table = dynamodb.Table('Orders')

# 3. Imprimir un mensaje de confirmación
print(f"Conectado a la tabla '{table.name}' en la región '{dynamodb.meta.client.meta.region_name}'.")


def create_order(order_id, customer_name, product, quantity, status):
    '''Crea un nuevo ítem en la tabla Orders.'''
    try:
        response = table.put_item(
           Item={
                'order_id': order_id,
                'customer_name': customer_name,
                'product': product,
                'quantity': quantity,
                'status': status,
                'order_date': '2025-11-11' # Puedes usar una fecha actual
            }
        )
        print(f"Pedido {order_id} creado exitosamente.")
        return response
    except Exception as e:
        print(f"Error al crear el pedido: {e}")

# create_order("ORD120","teclaoKK","tecalo",23,"Delivered")

def get_order(order_id):
    '''Obtiene un ítem de la tabla Orders por su ID.'''
    try:
        response = table.get_item(Key={'order_id': order_id})
        item = response.get('Item')
        if item:
            print(f"Datos del pedido {order_id}: {item}")
            return item
        else:
            print(f"No se encontró el pedido con ID {order_id}.")
            return None
    except Exception as e:
        print(f"Error al obtener el pedido: {e}")

# get_order("ORD120")

def update_order_status(order_id, new_status):
    '''Actualiza el atributo 'status' de un pedido.'''
    try:
        response = table.update_item(
            Key={'order_id': order_id},
            UpdateExpression="set #st = :s",
            ExpressionAttributeNames={'#st': 'status'},
            ExpressionAttributeValues={':s': new_status},
            ReturnValues="UPDATED_NEW"
        )
        print(f"Estado del pedido {order_id} actualizado a '{new_status}'.")
        return response
    except Exception as e:
        print(f"Error al actualizar el pedido: {e}")

# update_order_status("ORD120","Shipped")

def delete_order(order_id):
    '''Elimina un item de la tabla Orders.'''
    try:
        response = table.delete_item(Key={'order_id': order_id})
        print(f"Pedido {order_id} eliminado exitosamente.")
        return response
    except Exception as e:
        print(f"Error al eliminar el pedido: {e}")

# delete_order("ORD120")

orders_table = dynamodb.Table('Orders')

def get_orders_by_customer(customer_name):
    
    try:
        response = orders_table.scan(
            FilterExpression=Attr('customer_name').eq(customer_name)
        )
        
        orders = response.get('Items', [])
        
        print(f"Nombre: '{customer_name}':")
        for order in orders:
            print(order)
        
        return orders

    except Exception as e:
        print(f"Error al obtener los pedidos del cliente '{customer_name}': {e}")
        return []
    
# get_orders_by_customer("Carlos Soto")

if __name__ == "__main__":
    print("--- Demostración de operaciones con DynamoDB ---")

    # 1. Crear un nuevo pedido
    create_order("ORD-PY-1001", "Ana García", "Teclado Mecánico", 1, "Pending")

    # 2. Leer el pedido recién creado
    get_order("ORD-PY-1001")

    # 3. Actualizar su estado
    update_order_status("ORD-PY-1001", "Shipped")
    get_order("ORD-PY-1001") # Verificamos el cambio

    # 4. Buscar todos los pedidos de un cliente (usa un nombre que exista en tu tabla)
    get_orders_by_customer("Ana García")
    get_orders_by_customer("Carlos Soto") # Ejemplo con otro cliente

    # 5. Eliminar el pedido
    delete_order("ORD-PY-1001")
    get_order("ORD-PY-1001") # Verificamos que ya no existe

    print("\n--- Demostración finalizada ---")