import socket, json, threading, random, time
class NodoMaestro:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.limitarInventarioMax = 1000
        self.inventarioMaestro = {            
            "Fritos":               random.randint(0, self.limitarInventarioMax),
            "Cheetos":              random.randint(0, self.limitarInventarioMax),
            "Doritos":              random.randint(0, self.limitarInventarioMax),
            "Ruffles":              random.randint(0, self.limitarInventarioMax),
            "Tostitos":             random.randint(0, self.limitarInventarioMax),
            "Sabritas Adobadas":    random.randint(0, self.limitarInventarioMax),
            "Rancheritos":          random.randint(0, self.limitarInventarioMax),
            "Chocoretas":           random.randint(0, self.limitarInventarioMax),
            "Sabritas":             random.randint(0, self.limitarInventarioMax),
        }
        self.inventario = {}
        self.clientes = {}
        self.mutex = threading.Lock()
        self.mensajes = {}
        pass
    
    def iniciarServidor(self):
        #Crea un socket de tipo AF_INET (IPv4) y SOCK_STREAM (TCP)
        socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        """
        Enlaza el socket al self.host en el puerto self.port
        En el caso para obtener esta IP, lo conseguimos usando
        el comando ipconfig en la terminal de Windows 
        """
        socketServer.bind((self.host, self.port))
        # Escucha hasta 5 conexiones entrantes en el socket
        socketServer.listen(5)

        print(" Nodo Maestro esperando conexiones nueva Sucursal ".center(100,"="))

        while True:
            try:
                # Acepta una nueva conexión entrante y obtiene el socket del cliente y su dirección
                socketCliente, ipCliente = socketServer.accept()
                print(f"Nueva conexión con Sucursal con {ipCliente}")

                #Inicia un subproceso para manejar al cliente
                manejandoCliente = threading.Thread(target=self.atenderCliente, args=(socketCliente, ipCliente))
                manejandoCliente.start()
            except:
                print("Error de conexión con una sucursal")

    def atenderCliente(self, socketCliente, ipCliente):
        while True:
            try:
                # Recibe datos enviados por el cliente (hasta 1024 bytes)
                datos = socketCliente.recv(1024)

                # Si no se recibe ningún dato, se sale del bucle
                if not datos:
                    break

                # Decodifica los datos recibidos en formato UTF-8 para obtener el mensaje
                mensaje = datos.decode('utf-8')

                # Obtiene la marca de tiempo actual del servidor
                marcaTiempo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                # Muestra el mensaje del cliente junto con la marca  de tiempo y su dirección
                print(f"Mensaje de {ipCliente} ({marcaTiempo}): {mensaje}")

                # Almacena el mensaje en el diccionario de mensajes
                if ipCliente not in self.mensajes:    
                    self.mensajes[ipCliente] = []
                self.mensajes[ipCliente].append((marcaTiempo, mensaje))

                # Envia una respuesta al cliente confirmado la recepción del mensaje
                respuesta = f"Mensaje recibido de {ipCliente}"
                socketCliente.send(respuesta.encode('utf-8'))

            except Exception as error:
                #Si ocurre un error, se muestra en la consola y se sale del bucle
                print(f"Error de conexión con {ipCliente}, ocurrio el error: {error}")
                break
    def distribuirAutomaticamente(self):
        pass
    
    def procesarMensaje(self):
        pass
    
    def agregarSucursal(self):
        pass
    
    def comprarArticulo(self):
        pass

nodoMaestro = NodoMaestro("192.168.100.5", 5000)
nodoMaestro.iniciarServidor()