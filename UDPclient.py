import json
import os
import platform
from datetime import datetime
from socket import *

def main():
    serverName = 'localhost'
    serverPort = 3027
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    debug = 1
    print("=== FATONG Heart Disease Prediction ===")
    print('Provide the following information by integer')

    if debug != 1:
        while(1) :
            try:
                age = int(input('Input Age: '))
                break
            except ValueError:
                print('Please enter an integer')

        while(1) :
            try:
                sex = int(input('Input Sex (1=male, 0=female): '))
                break
            except ValueError:
                print('Please enter an integer')

        while(1) :
            try:
                chest_pain_type = int(input('Input chest pain type (1=typical angina, 2=atypical angina, 3=non-anginal pain, 4=asymptomatic): '))
                break
            except ValueError:
                print('Please enter an integer')

        while(1) :
            try:
                bp = int(input('Input resting blood pressure (in mmHg): '))
                break
            except ValueError:
                print('Please enter an integer')

        while(1) :
            try:
                cholesterol = int(input('Input serum cholestoral (in mg/dl): '))
                break
            except ValueError:
                print('Please enter an integer')

        while(1) :
            try:
                fbs = int(input('Fasting blood sugar > 120 mg/dl (1=true; 0=false): '))
                break
            except ValueError:
                print('Please enter an integer')

        while(1) :
            try:
                ekg_result = int(input('input resting electrocardiographic results (0=normal, 1=having ST-T wave abnormality, 2=showing probable left ventricular hypertrophy by Estes criteria): '))
                break
            except ValueError:
                print('Please enter an integer')        

        while(1) :
            try:
                max_hr = int(input('Input maximum heart rate achieved: '))
                break
            except ValueError:
                print('Please enter an integer')

        while(1) :
            try:
                exercise_angina = int(input('Exercise induced angina (1=yes; 0=no): '))
                break
            except ValueError:
                print('Please enter an integer')   

        while(1) :
            try:
                st_depression = float(input('Input ST depression induced by exercise relative to rest (decical value**): '))
                break
            except ValueError:
                print('Please enter a decimal')   
        
        while(1) :
            try:
                slope_of_st = int(input('Input the slope of the peak exercise ST segment (1=upsloping, 2=flat, 3=downsloping): '))
                break
            except ValueError:
                print('Please enter an integer')   
        
        while(1) :
            try:
                number_of_vessels_fluro = int(input('Input the number of major vessels colored by flourosopy (0-3): '))
                break
            except ValueError:
                print('Please enter an integer')   
        
        while(1) :
            try:
                thallium = int(input('Input Thallium  (3=normal, 6=fixed defect, 7=reversable defect): '))
                break
            except ValueError:
                print('Please enter an integer')   

    # information = json.dumps({'Age' : age, 'Sex' : sex, 'Chest pain type' : chest_pain_type, 'BP' : bp, 'Cholesterol' : cholesterol, 'FBS over 120' : fbs, 'EKG results' : ekg_result, 'Max HR' : max_hr, 'Exercise angina' : exercise_angina, 
    # 'ST depression' : st_depression, 'Slope of ST' : slope_of_st, 'Number of vessels fluro' : number_of_vessels_fluro, 'Thallium' : thallium}).encode('utf-8')
    
    features = {'Age' : 21, 'Sex' : 1, 'Chest pain type' : 1, 'BP' : 120, 'Cholesterol' : 180, 'FBS over 120' : 0, 'EKG results' : 0, 'Max HR' : 120, 'Exercise angina' : 1, 
    'ST depression' : 1.0, 'Slope of ST' : 1, 'Number of vessels fluro' : 3, 'Thallium' : 3}
    response_headers_raw = {
        'status_code': 200,
        'action' : 'PRT (PREDICT) DATASET',
        'host': os.name + '/' + platform.system() + '/' + platform.release(),
        'time' : datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        'feature_set' : 13,
        'model' : 'Decision tree'
    }

    information = json.dumps([features, response_headers_raw]).encode('utf-8')

    clientSocket.sendto(information, (serverName, serverPort))
    modifiedInformation, serverAddress = clientSocket.recvfrom(2048) 

    result = modifiedInformation.decode().split('\n')[-2].split(' ')[1]
    print("\nYour heart disease prediction result:", result)
    clientSocket.close()

if __name__ == "__main__":
    main()