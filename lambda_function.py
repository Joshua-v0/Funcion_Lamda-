import json
import boto3
from botocore.exceptions import ClientError
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PrestamosLibros')

def lambda_handler(event, context):
    # Imprimir el evento recibido para depuración
    print(f"Evento recibido: {json.dumps(event)}")
    
    required_fields = ["usuario", "libro", "fecha_prestamo", "fecha_devolucion"]
    
    for field in required_fields:
        if field not in event:
            return {
                'statusCode': 400,
                'body': json.dumps(f"Falta el campo: {field}")
            }

    # Generar usuarioID si no está presente en el evento
    usuarioID = str(event.get('usuarioID', str(uuid.uuid4())))
    
    usuario = event['usuario']
    libroID = event['libro']  # Se usa 'libro' del evento como 'libroID' en la tabla
    fecha_prestamo = event['fecha_prestamo']
    fecha_devolucion = event['fecha_devolucion']

    try:
        response = table.put_item(
            Item={
                'usuarioID': usuarioID,
                'libroID': libroID,
                'usuario': usuario,
                'fecha_prestamo': fecha_prestamo,
                'fecha_devolucion': fecha_devolucion
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps("Préstamo registrado con éxito")
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error al registrar el préstamo: {e.response['Error']['Message']}")
        }
