# from ezoptic_matching_algo_TRAIN import call_face_api
import http.client, urllib.request, urllib.parse, urllib.error, base64
import pandas as pd
import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier
import pickle

# save = [FACE_COLS, FACE_DF, FACE_CLF]

def call_face_api(url):
    
    url = "'" + url + "'"
    
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'd6dbd454b75d44e098550af6845fc347',
    }
    
    params = urllib.parse.urlencode({
    # Request parameters
    'returnFaceLandmarks': 'true',
    })
    
    try:
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, """{"url": """ + url + """}""", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        data = data.decode("utf-8") 
        return data
    
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return False

def match_face_glasses(url, face_cols, face_df, face_clf):
    url = url.replace("'", '"""')
    
    output = call_face_api(url)
    
    if output == '[]':
        return "Face image could not be processed. Please upload a better quality image"
    
    df = pd.DataFrame(np.zeros(shape=(1,len(face_cols))), columns=face_cols)
    
    col_num = 0
    
    for i in range(len(output)):
        char = output[i]

        if (char == 'x' or char == 'y') and output[i-1] == '"':
            num = ''

            num_index = i + 3

            digit = output[num_index]

            while digit not in ',{}' and num_index <= len(output)-1:
                num += digit

                num_index += 1

                digit = output[num_index]
            df.iloc[0][col_num] = float(num)

            col_num += 1
            
    pred = face_clf.predict(df[df.columns])
           
    # print("Length", type(face_df['glassesShape'][pred]))
    # print(face_df['glassesShape'][pred].values)
    return face_df['glassesShape'][pred].values[0]
