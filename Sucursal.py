import socket,json,time

class NodoSucursal:
    # Inicializa la sucursal con la dirección, puerto y nombre de la sucursal especificada
    def __init__(self, host, port, sucursal):
        self.host = host
        self.port = port
        self.sucursal = sucursal
        #Crea un nuevo socker de la sucursal
        self.miSocket = socket.socket()

    def main(self):
        # Establece una conexión con el Nodo Maestro en self.host y el puerto self.port
        self.miSocket.connect((self.host, self.port))
        while True:
            # Obtiene un mensaje ingresado por el usuario
            mensaje = str(input("Escribe un mensaje: "))
            
            # Se agrega un Try - Except, ya que se considera el caso en el que el Nodo Maestro se desconecta a midad
            # del proceso, así que es mejor tambien finalizar la actividad del cliente con el servidor.
            try:
                # Llama al metodo 'enviarMensaje' para enviar el mensaje al Nodo Maestro
                self.enviarMensaje(mensaje)
                
                # Recibe una respuesta del Nodo Maestro (hasta 1024 bytes) y la decodifica
                respuesta = self.miSocket.recv(1024)
                print(respuesta.decode('utf-8'))

            # Cuando se interrumpe la comunicación con el Nodo Maestro, se finaliza la petición de más mensajes
            # y esto provoca que el programa al igual finalice de este lado
            except ConnectionResetError as error:
                print(f"Se interrumpio la conexión con el Nodo Maestro")
                break
        self.miSocket.close()

    def enviarMensaje(self, mensaje):
        # Obtiene la marca de tiempo actual del cliente
        tiempoProcesado = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # Construye el mensaje concatenando la marca de tiempo con el mensaje original
        mensajeCompleto = f"[{tiempoProcesado}] {mensaje}"
        
        # Envia el mensaje al Nodo Maestro como bytes codificados en UTF-8
        self.miSocket.send(mensajeCompleto.encode('utf-8'))

nuevaSucursal = NodoSucursal("192.168.100.5", 5001, "sucursal_CDMX")
nuevaSucursal.main()