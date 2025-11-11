import boto3

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

get_order("ORD120")