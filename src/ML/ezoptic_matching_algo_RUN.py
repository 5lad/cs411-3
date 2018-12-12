from ezoptic_matching_algo_TRAIN import call_face_api
import http.client, urllib.request, urllib.parse, urllib.error, base64
import pandas as pd
import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier
import pickle

# save = [FACE_COLS, FACE_DF, FACE_CLF]
with open("save.pickle", 'wb') as f:
    import pickle
    save = pickle.load(f)

def match_face_glasses(url, face_cols=save[0], face_df=save[1], face_clf=save[2]):
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
            
    return face_df['glassesShape'][pred][0]
