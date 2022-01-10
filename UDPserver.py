from socket import *
import pickle
import numpy as np
import json

loaded_model = pickle.load(open('heart-disease-model.pkl', 'rb'))

def predictHD(featureSet):
    dict = json.loads(featureSet)
    items = dict.values()
    features = list(items)
    to_predict = np.array(features).reshape(1, 13)
    result = loaded_model.predict(to_predict)

    return result[0]

def startServer(serverPort):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print('Server is ready to receive')
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        print('=== Information received ===')
        print(message.decode())
        result = predictHD(message.decode())
        serverSocket.sendto(result.encode(), clientAddress)
        print(f'send result back to {clientAddress}')
        print("\nWaiting for next request")
        print("========================")

def main():
    port = 3027
    startServer(port)

if __name__ == "__main__":
    main()