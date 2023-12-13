import socket,json,time
from sys import argv
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
        self.soyLasSucursal()
        while True:
            # Menu de opciones
            print(f" Menú de sucursal {self.sucursal} ".center(100, "#"))
            print("1. Comprar articulo")
            print("2. Agregar articulo")
            print("3. Consultar clientes")
            print("9. Salir")
            opcion = int(input("Opción: "))
            
            # Switch para afectar la variable mensaje según la opción seleccionada
            if opcion == 1:
                mensaje = "comprarArticulo"
            elif opcion == 2:
                mensaje = "agregarArticulo"
                articulo = str(input("Agrega el nombre del articulo por ingresar: "))
                cantArt = str(input(f"Cuantos piezas agregaras de {articulo}? "))
            elif opcion == 3:
                mensaje = "consultarCliente"
            elif opcion == 9:
                mensaje = "salir"
            else:
                print("Opción inválida. Intente nuevamente.")
                continue
            
            # Se agrega un Try - Except, ya que se considera el caso en el que el Nodo Maestro se desconecta a midad
            # del proceso, así que es mejor tambien finalizar la actividad del cliente con el servidor.
            try:

                # Llama al metodo 'enviarMensaje' para enviar el mensaje al Nodo Maestro
                self.enviarMensaje(mensaje)
                
                if mensaje == "comprarArticulo":
                    time.sleep(0.3)
                    # Recibe una respuesta del Nodo Maestro (hasta 1024 bytes) y la decodifica
                    respuesta = self.miSocket.recv(1024)
                    # # Se decodifica la respuesta y se convierte a un diccionario
                    respuesta = respuesta.decode('utf-8')
                    respuesta = json.loads(respuesta)
                    # # Se imprime el diccionario
                    print(f" Producto Disponible ".center(100,"-"))
                    print(respuesta)
                    for indice, producto, in enumerate(respuesta[self.sucursal], start=1):
                        if respuesta[self.sucursal][producto]>0:
                            print(f"{indice}.- {producto}")
                    articulo = str(input("Que producto te gustaría comprar? Respuesta = "))
                    cantArt = str(input(f"Cuantos piezas compraras de {articulo}? Respuesta = "))
                    usuarioCliente = str(input("Agrega tu usuario: "))
                    
                    # Si se quiere comprar o agregar un artículo, recibe los datos del artículo y lo envía a la
                    # sucursal correspondiente
                    self.enviarMensaje(articulo)
                    # Se agrega un pequeño sleep, ya que si no se agrega, el mensaje anterior y posterior a esta linea, se manda
                    # concatenados, provocando que en el nodo maestro, no se reciba un mensaje, haciendo que se quede esperando 
                    time.sleep(0.3)
                    self.enviarMensaje(cantArt)
                    # Se agrega un pequeño sleep, ya que si no se agrega, el mensaje anterior y posterior a esta linea, se manda
                    # concatenados, provocando que en el nodo maestro, no se reciba un mensaje, haciendo que se quede esperando 
                    time.sleep(0.3)
                    self.enviarMensaje(usuarioCliente)
                    time.sleep(0.2)
                    respuesta = self.miSocket.recv(1024)
                    respuesta = respuesta.decode('utf-8')
                    print(respuesta)
                    time.sleep(0.3)
                if mensaje == "agregarArticulo":
                    # Si se quiere comprar o agregar un artículo, recibe los datos del artículo y lo envía a la
                    # sucursal correspondiente
                    self.enviarMensaje(articulo)
                    # Se agrega un pequeño sleep, ya que si no se agrega, el mensaje anterior y posterior a esta linea, se manda
                    # concatenados, provocando que en el nodo maestro, no se reciba un mensaje, haciendo que se quede esperando 
                    time.sleep(0.3)
                    self.enviarMensaje(cantArt)
                    time.sleep(0.3)
                if mensaje == "consultarCliente":
                    # Se recibirá un diccionario que nos enviará el nodo maestro
                    # Aqui recibiremos el diccionario
                    # Se agrega un pequeño sleep, ya que si no se agrega, el mensaje anterior y posterior a esta linea, se manda
                    # concatenados, provocando que en el nodo maestro, no se reciba un mensaje, haciendo que se quede esperando
                    time.sleep(0.3)
                    # Recibe una respuesta del Nodo Maestro (hasta 1024 bytes) y la decodifica
                    respuesta = self.miSocket.recv(1024)
                    # # Se decodifica la respuesta y se convierte a un diccionario
                    respuesta = respuesta.decode('utf-8')
                    respuesta = json.loads(respuesta)
                    # # Se imprime el diccionario
                    print(" USUARIOS ".center(50,"-"))
                    for indice, usuario in enumerate(respuesta,start=1):
                        print(f"{indice}.- {usuario}")                     
 
                    # # Se agrega un pequeño sleep, ya que si no se agrega, el mensaje anterior y posterior a esta linea, se manda
                    # # concatenados, provocando que en el nodo maestro, no se reciba un mensaje, haciendo que se quede esperando
                    time.sleep(0.2) 
                    pass
                
                # Recibe una respuesta del Nodo Maestro (hasta 1024 bytes) y la decodifica
                respuesta = self.miSocket.recv(1024)
                print(respuesta.decode('utf-8'))

                if mensaje == "salir":
                    print(f"Cerrando conexión con de esta sucursal")
                    break
            # Cuando se interrumpe la comunicación con el Nodo Maestro, se finaliza la petición de más mensajes
            # y esto provoca que el programa al igual finalice de este lado
            except Exception as error:
                print(f"Se interrumpio la conexión con el Nodo Maestro")
                break
        self.miSocket.close()

    def enviarMensaje(self, mensaje):
        # Obtiene la marca de tiempo actual del cliente
        tiempoProcesado = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # Construye el mensaje concatenando la marca de tiempo con el mensaje original
        mensajeCompleto = f"[{tiempoProcesado}] {mensaje}"
        
        # Envia el mensaje al Nodo Maestro como bytes codificados en UTF-8
        time.sleep(0.3)
        self.miSocket.send(mensaje.encode('utf-8'))
        time.sleep(0.3)
    def soyLasSucursal(self):
        # Envia el nombre de la sucursal al Nodo Maestro
        time.sleep(0.3)
        self.miSocket.send(self.sucursal.encode('utf-8'))
        time.sleep(0.3)
nuevaSucursal = NodoSucursal(str(argv[1]), 5000, f"sucursal_{argv[2].upper()}")
nuevaSucursal.main()
