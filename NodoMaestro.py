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
        self.logsSucursalesDisponibles = {}
        self.sucursalIP = {}
        self.clientesYSusGuiasDeEnvio = {}
        self.historialGuiaEnvio = {}
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
                socketCliente, ipSucursal = socketServer.accept()
                print(f"Nueva conexión con Sucursal con {ipSucursal}")

                #Inicia un subproceso para manejar al cliente
                manejandoCliente = threading.Thread(target=self.atenderCliente, args=(socketCliente, ipSucursal))
                manejandoCliente.start()
                
            except:
                print("Error de conexión con una sucursal")

    def atenderCliente(self, socketCliente, ipSucursal):
        # Agregar la sucursal de la IP
        suc = socketCliente.recv(1024)
        suc = suc.decode('utf-8')
        self.agregarSucursal(suc)
        self.asignarIPaSucursal(suc, ipSucursal)
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
                print(f"Mensaje de {ipSucursal} ({marcaTiempo}): {mensaje}")
                
                # El mensaje, realiza una instrucción en el Nodo Maestro
                self.procesarMensaje(mensaje,ipSucursal, socketCliente)
                #Despues de cualquier acción, realizamos la distribución
                self.distribuirAutomaticamente()

                # Verifica si el mensaje indica que la conexión debe cerrarse
                if mensaje == "salir":
                    print(f"Cerrando conexión con {ipSucursal}")
                    break
                # Almacena el mensaje en el diccionario de mensajes
                if ipSucursal not in self.logsSucursalesDisponibles:    
                    self.logsSucursalesDisponibles[ipSucursal] = []
                self.logsSucursalesDisponibles[ipSucursal].append((marcaTiempo, mensaje))
                # Envia una respuesta al cliente confirmado la recepción del mensaje
                time.sleep(0.2) 
                respuesta = f"Mensaje recibido de {ipSucursal}"
                socketCliente.send(respuesta.encode('utf-8'))
            except Exception as error:
                #Si ocurre un error, se muestra en la consola y se sale del bucle
                print(f"Ocurrio el error: {error}")
                # Cuando se desconecta el cliente, dejará de ser considerado en la lista de sucursales 
                self.seDesconectoUnaSucursal(ipSucursal)
                break
        # Cierra la conexión con el cliente al finalizar
        socketCliente.close()
        if not self.sucursalIP:
            print("Ya no hay sucursales")
        else:
           self.distribuirAutomaticamente() 
            #Se agregara un metodo para finalizar el programa por completo
    
    def asignarIPaSucursal(self, nombreSucursal, IPSucursal):
        self.sucursalIP[IPSucursal] = nombreSucursal

    def distribuirAutomaticamente(self):
        for producto, cantidad in self.inventarioMaestro.items():
            if len(self.inventario) != 0:
                for sucursal in self.inventario:
                    self.inventario[sucursal][producto] = 0
        # Distribuye equitativamente el inventario del Nodo Maestro en los nodos existentes                    
        for producto, cantidad in self.inventarioMaestro.items():
            if len(self.inventario) != 0:
                cantidad_por_sucursal = cantidad // len(self.inventario)
                for sucursal in self.inventario:
                    self.inventario[sucursal][producto] += cantidad_por_sucursal
                self.inventario[sucursal][producto] += cantidad%len(self.inventario)
        #print(self.inventario)            
    
    def seDesconectoUnaSucursal(self,ipSucursal):
        print(f"Se desconectó la sucursal {self.sucursalIP[ipSucursal]}")
        self.logsSucursalesDisponibles.pop(ipSucursal)
        self.sucursalIP.pop(ipSucursal)

    def procesarMensaje(self, instruccionDeLaSucursal,ipSucursal, socketCliente):
        if instruccionDeLaSucursal == "salir":
            self.seDesconectoUnaSucursal(ipSucursal)
        elif instruccionDeLaSucursal == "agregarArticulo":
            self.agregarArticulo(socketCliente)
        elif instruccionDeLaSucursal == "comprarArticulo":
            self.comprarArticulo(socketCliente,ipSucursal)
        elif instruccionDeLaSucursal == "consultarCliente":
            self.consultarClientes(socketCliente)
    
    def agregarSucursal(self, sucursal):
        self.inventario[sucursal] = {
            "Fritos": 0,
                "Cheetos": 0,
                "Doritos": 0,
                "Ruffles": 0,
                "Tostitos": 0,
                "Sabritas Adobadas": 0,
                "Rancheritos": 0,
                "Chocoretas": 0,
                "Sabritas": 0,
        }
    
    def comprarArticulo(self,socketCliente,ipSucursal):
        articulo = socketCliente.recv(1024)
        articulo = articulo.decode('utf-8')
        cantArt = socketCliente.recv(1024)
        cantArt = int(cantArt.decode('utf-8'))
        usuario = socketCliente.recv(1024)
        usuario = str(usuario.decode('utf-8'))
        print(f"El usuario {usuario} quiere comprar {cantArt} piezas de {articulo}".center(100,"❁"))
        self.mutex.acquire()
        try:
            if self.inventarioMaestro[articulo] - cantArt >= 0 and articulo in self.inventarioMaestro:
                print(" Se compra lo siguiente ".center(100,"-"))
                compras = f"Articulo: {articulo}\tCantidad: {cantArt}"
                print(compras)
                self.inventarioMaestro[articulo] -= cantArt
                idEnvio = f"{str(hash(articulo))[15:]}/{str(hash(usuario))[15:]}/{self.sucursalIP[ipSucursal]}/{usuario}"
                self.cliente(usuario,idEnvio, compras)
            else:
                print(f"El articulo {articulo} no existe o no hay inventario suficiente")  
        finally:
            print(self.inventarioMaestro)
            self.mutex.release()
    
    def cliente(self,usuario,idEnvio, compras):
        # Si no existe el usuario en el diccionario self.clientesYSusGuiasDeEnvio
        # Se crea la llave con el usuario y se hara un registro de todos sus idEnvio
        if usuario not in self.clientesYSusGuiasDeEnvio:
            self.clientesYSusGuiasDeEnvio[usuario] = []
        # Agregamos el idEnvio con su respectivo usuario
        self.clientesYSusGuiasDeEnvio[usuario].append(idEnvio)
        # Se crea un diccionario con el idEnvio y su respectivo estado
        self.historialGuiaEnvio[idEnvio] = compras
        print(f"Historial de clientes: {self.clientesYSusGuiasDeEnvio}")
        print(f"Historial de guía de envíos {self.historialGuiaEnvio}")
        
    def consultarClientes(self, socketCliente):
        # Se envía el diccionario de clientes
        socketCliente.send(json.dumps(self.clientesYSusGuiasDeEnvio).encode('utf-8'))

    def agregarArticulo(self,socketCliente):
        articulo = socketCliente.recv(1024)
        articulo = articulo.decode('utf-8')
        cantArt = socketCliente.recv(1024)
        cantArt = int(cantArt.decode('utf-8'))
        print(" Se agrega al inventario lo siguiente ".center(100,"-"))
        print(f"Articulo: {articulo}\tCantidad: {cantArt}")
        self.mutex.acquire()
        try:
            if articulo in self.inventarioMaestro:
                self.inventarioMaestro[articulo] += cantArt   
            else:
                self.inventarioMaestro[articulo] = cantArt
        finally:
            print(self.inventarioMaestro)
            self.mutex.release()

nodoMaestro = NodoMaestro("192.168.100.5", 5000)
nodoMaestro.iniciarServidor()