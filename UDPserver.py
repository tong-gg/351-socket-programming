from socket import *
import pickle
import numpy as np
import json
import os
import platform
from datetime import datetime

loaded_model = pickle.load(open('heart-disease-model.pkl', 'rb'))

def formatMsgUtil(dict_msg):
    msg = ""
    for key in dict_msg:
        msg += "{key}: {value}\r\n".format(key=key, value=dict_msg[key])

    msg += "data_length: {msg_size}\r\n".format(msg_size = str(len(dict_msg['result'].encode('utf-8'))))
    return msg

def responseHeader(payload, code):
    status_msg = ''
    if code == 200:
        status_msg = '200 PRT OK!/FATONG 1.0'
    elif code == 250:
        status_msg = '250 PRT FATAL'

    response = {
        'status': code,
        'status_msg': status_msg,
        'Server': "{os_name}/{system}/{release}".format(os_name = os.name, system = platform.system(), release = platform.release()),
        'Time': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'Feature set': len(payload[0]),
        'Model': 'Decision Tree'
    }

    return response

def predictHD(payload):
    items = payload[0].values()
    features = list(items)
    if len(features) == 13:
        to_predict = np.array(features).reshape(1, 13)
        result = loaded_model.predict(to_predict)
        code = 'ok'
    else:
        result = ['Cannot predict']
        code = 'error'

    if code == 'ok':
        response = responseHeader(payload, 200)
    else:
        response = responseHeader(payload, 250)

    return result[0], response

def startServer(serverPort):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print('Server is ready to receive')

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        print('Connected!')
        print('=== Information received ===')
        print(message.decode())
        payload = json.loads(message.decode())
        feature = payload[0]
        header = payload[1]

        if header['action'] == "PRT (PREDICT) DATASET":
            result, response_raw = predictHD(payload)
            response_raw['result'] = result
            msg = formatMsgUtil(response_raw)
        
        serverSocket.sendto(msg.encode(), clientAddress)
        print(f'send result back to {clientAddress}')
        print("\nWaiting for next request")
        print("========================")

def main():
    port = 3027
    startServer(port)

if __name__ == "__main__":
    main()