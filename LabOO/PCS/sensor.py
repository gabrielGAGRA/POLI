import serial
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import initialize_app
from time import sleep

def read_sensor():
    try:
        if ser.isOpen():
            while True:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').rstrip()
                    data = data[:12]
                    print(f"Sensor Data: {data}")
                    
                    product_ref = ref.child(data)
                    product = product_ref.get()
                    
                    if product:
                        #se produto ja esta na base e tem mais que 0, remove uma unidade
                        if product.get('quantity', 0) > 0:
                            new_quantity = product.get('quantity', 0) - 1
                            product_ref.update({'quantity': new_quantity})
                        #se ja esta na base e tem 0, vai adicionar uma unidade
                        else:
                            new_quantity = product.get('quantity') + 1
                            product_ref.update({'quantity': new_quantity})
                    
                    #se nao estiver na base, adicionara o produto com quantidade 1
                    else:
                        product_ref.set({
                            'codigo': data,
                            'quantity': 1,
                            'nome': 'Produto',
                        })
                sleep(1)
    finally:
        ser.close()
        
ser = serial.Serial(
    port='/dev/ttyS0', 
    baudrate=9600,    
    timeout=1
)

# Initialize Firebase
cred = credentials.Certificate(r'C:Users\.json')
initialize_app(cred, {
    'databaseURL': 'https://psc3100dc58b-default-rtdb.firebaseio.com/'
})

# Branch que vai ser guardado
ref = db.reference('App')

read_sensor()