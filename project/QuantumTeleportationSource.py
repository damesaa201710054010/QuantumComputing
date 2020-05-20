#Daniel Mesa
#Implementacion del protocolo de teleportacion cuantica, difiere un poco a qiskit por el hecho de que el principio pasamos un entero que representa
#un bit que luego es convertido en qubit segun su estado
#Realizamos la importacion de las lobrerias necesarias para la impementacion
from projectq.ops import All, CNOT, H, Measure, X, Z #Librerias necesarias para la implmentacion de simulaciones de circuitos cuanticos
from projectq import MainEngine   #Libreria para la simulacion de ejecucion de circuitos Cuanticos


#Creamos algunas funciones que faciliten la division de los pasos a tener en cuenta

#Creamos los pasos iniciales para el aplicamiento de la teoria de bell: el par de bell
def parDeBell(quantum_engine):

    #Creamos dos qubits para el envio t decodificacion de alice y bob resectivamente
    q1 = quantum_engine.allocate_qubit()
    q2 = quantum_engine.allocate_qubit()
    #Igual que el circuito diseñado con qiskit aplicamos la compuerta H para llevarlo al estado |+>
    H | q1

    #El segundo qubit es llevado al estado 1
    CNOT | (q1, q2)

    return q1, q2


#se crea un mensaje con el valor del mensaje, que es 0 o 1 y se entrelaza con el qubit que es tomado del entrelazamiento
#luego se convierten en 2 bits clasicos que son enviados a traves de un canal clasico como la teoria lo dicta
def enviarMensaje(quantum_engine , q1, mensaje):
    q3 = quantum_engine.allocate_qubit()
    if mensaje == 1:
        #el qubit es convetido en 1 si el mensaje es 1 con la compuesta Pauli-X
        X | q3

    #Entrelazamiento del qubit con el mensaje
    CNOT | (q3, q1)

    #Ponemos el qubit de mensaje en superposicion y luego medimos la salida de los dos valores de bits clasicos, colapsando los estados

    H | q3
    Measure | q3
    Measure | q1

    #Se envian los bits clasicos a traves de un canal clasico, pero codificado
    mensajeCodificado = [int(q3), int(q1)]

    return mensajeCodificado

#En esta funcion bob decodifica el mensaje mediante el segundo qubit aplicando Pauli-X o Pauli-Z
#Cabe aclarar que el mensaje puede ser decodificado debido a que se conoce como fue polarizado el mensaje
def recibirMensaje(quantum_engine, mensaje, q2):
    if mensaje[1] == 1:
        X | q2
    if mensaje[0] == 1:
        Z | q2

    #Se realiza la medicion colapsando el estado
    Measure | q2

    quantum_engine.flush()
    bitRecibido = int(q2)

    #se retorna el resultado
    return bitRecibido

#iniciamos la ejecucion de la simulacion, creando un circuito
quantum_engine=MainEngine()
mensaje = 1#Mensaje que enviaremos
print('Mensaje enviado: ', mensaje) 
#creamos los dos qubits necesarios
q1, q2 = parDeBell(quantum_engine)
#Codificamos el mensaje
mensajeCodificado = enviarMensaje(quantum_engine=quantum_engine, q1=q1, mensaje=mensaje)
#Decodificamos el mensaje
print('Mensaje Recibido: ', recibirMensaje(quantum_engine, mensajeCodificado, q2))