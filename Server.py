import socket
import time
from _thread import start_new_thread
import os
import json

def printScores():
    os.system("clear")
    print("Connected", len(clients), "client(s): ")
    for player in scores:
        print(player, scores.get(player))

def multi_threaded_client(connection):
    global endedPlayers, clients, scores

    while True:
        data = connection.recv(1024)
        text = data.decode("utf-8").split(" ")
        if(text[0] == "END"):
            endedPlayers += 1
            if(endedPlayers==len(clients)):
                for client in clients.keys():
                    client.send("SCORES".encode("utf-8"))
                    scores_encoded = json.dumps(scores).encode('utf-8')
                    client.send(scores_encoded)

        elif(len(text) == 1 and len(text[0]) != 0):
            
            clients.update({connection: text[0]})
            scores.update({text[0]:"0"})

        elif(len(text) == 2):
            scores.update({text[0]:text[1]})
        elif not data:
            scores.pop(clients.get(connection))
            clients.pop(connection)
            if(len(clients)==0):
                endedPlayers = 0
                resetAll()
            printScores()
            break
        printScores()
    connection.close()

def resetAll():
    global clients, scores
    time.sleep(1)   # xD    Nie wiem czemu, ale dziala. Pewnie race condition
    clients = {"":""}
    clients.clear()
    scores = {"":""}
    scores.clear()

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bound = False
while not bound:
    try:
        server_socket.bind(('0.0.0.0', 8015))
        bound = True
        print("Started server :)")
    except OSError:
        print("Failed to bind, trying again in 1 seconds...")
        time.sleep(1)   # xD
server_socket.listen(1)

clients = {"":""}
clients.clear()
scores = {"":""}
scores.clear()

endedPlayers = 0

while True:
    try:
        (Client, address) = server_socket.accept()
        clients.update({Client: "Unknown"})
        start_new_thread(multi_threaded_client, (Client, ))

        if(len(clients) == 2):
            time.sleep(1)   # xD
            print("STARTED GAME")
            for client in clients.keys():
                client.send("START".encode("utf-8"))
    except:
        server_socket.shutdown(socket.SHUT_RDWR)
        server_socket.close()
