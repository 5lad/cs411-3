# LIBRARIES:
import http.client, urllib.request, urllib.parse, urllib.error, base64

import pandas as pd
import numpy as np

import random

from sklearn.ensemble import RandomForestClassifier
import pickle
def call_face_api(url):
    
    url = "'" + url + "'"
    
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '89595999865a46fa9ab02ed24e27f23f',
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


# GLOBAL VARIABLES:
FACE_COLS = []

NUM_IMGS = 173

IMG_URLS = ["""https://i.imgur.com/MOWKFmH.jpg""",
"""https://i.imgur.com/pz5PPGe.jpg""",
"""https://i.imgur.com/PMzYIWp.jpg""",
"""https://i.imgur.com/jMXK2pp.jpg""",
"""https://i.imgur.com/Fk68XYx.jpg""",
"""https://i.imgur.com/vc4aioP.jpg""",
"""https://i.imgur.com/2SAwCKA.jpg""",
"""https://i.imgur.com/uLsdNNb.jpg""",
"""https://i.imgur.com/VBsKrfn.jpg""",
"""https://i.imgur.com/uoP5Q1S.jpg""",
"""https://i.imgur.com/45kfPNT.jpg""",
"""https://i.imgur.com/m6HxqHq.jpg""",
"""https://i.imgur.com/BJQfTG1.jpg""",
"""https://i.imgur.com/lwM0IKU.jpg""",
"""https://i.imgur.com/TFytNEQ.jpg""",
"""https://i.imgur.com/8d9PzlJ.jpg""",
"""https://i.imgur.com/ZjeFski.jpg""",
"""https://i.imgur.com/HVljKpP.jpg""",
"""https://i.imgur.com/YM9Fg46.jpg""",
"""https://i.imgur.com/ugQUl9d.jpg""",
"""https://i.imgur.com/xcfWkno.jpg""",
"""https://i.imgur.com/7YdzIhr.jpg""",
"""https://i.imgur.com/AsdmhFX.jpg""",
"""https://i.imgur.com/NeOgiWc.jpg""",
"""https://i.imgur.com/sQWIGZd.jpg""",
"""https://i.imgur.com/ppof1Lp.jpg""",
"""https://i.imgur.com/f8l0JhN.jpg""",
"""https://i.imgur.com/9GIxyQ3.jpg""",
"""https://i.imgur.com/GxSUSBF.jpg""",
"""https://i.imgur.com/yov5MKF.jpg""",
"""https://i.imgur.com/xjLYdOn.jpg""",
"""https://i.imgur.com/WVNNITU.jpg""",
"""https://i.imgur.com/i1lBVzV.jpg""",
"""https://i.imgur.com/FzLLBlB.jpg""",
"""https://i.imgur.com/8OjMUfO.jpg""",
"""https://i.imgur.com/ElbOvVS.jpg""",
"""https://i.imgur.com/wuCnZ3x.jpg""",
"""https://i.imgur.com/VW7dGd5.jpg""",
"""https://i.imgur.com/9TY4GSM.jpg""",
"""https://i.imgur.com/mrgm0YG.jpg""",
"""https://i.imgur.com/z3yfJku.jpg""",
"""https://i.imgur.com/Z6pJjRq.jpg""",
"""https://i.imgur.com/DDp0Fbs.jpg""",
"""https://i.imgur.com/KUAcHP0.jpg""",
"""https://i.imgur.com/IC10AhH.jpg""",
"""https://i.imgur.com/Eqcw9pc.jpg""",
"""https://i.imgur.com/exsSB9f.jpg""",
"""https://i.imgur.com/CWyG2Lm.jpg""",
"""https://i.imgur.com/JFuQfsq.jpg""",
"""https://i.imgur.com/Gea0HmW.jpg""",
"""https://i.imgur.com/OWWKRwt.jpg""",
"""https://i.imgur.com/3nyKkWb.jpg""",
"""https://i.imgur.com/hzUMVhj.jpg""",
"""https://i.imgur.com/6Tbr6l2.jpg""",
"""https://i.imgur.com/BxprPc3.jpg""",
"""https://i.imgur.com/gr0INiH.jpg""",
"""https://i.imgur.com/XZhFidu.jpg""",
"""https://i.imgur.com/v8UvocI.jpg""",
"""https://i.imgur.com/lRt8NWA.jpg""",
"""https://i.imgur.com/K7WoQe7.jpg""",
"""https://i.imgur.com/DKROuei.jpg""",
"""https://i.imgur.com/VTASDoi.jpg""",
"""https://i.imgur.com/HV9wHBd.jpg""",
"""https://i.imgur.com/7g4U6Kg.jpg""",
"""https://i.imgur.com/O1SWQmu.jpg""",
"""https://i.imgur.com/uV2OhC8.jpg""",
"""https://i.imgur.com/gZFG0z4.jpg""",
"""https://i.imgur.com/fkWl130.jpg""",
"""https://i.imgur.com/WM8Fwc4.jpg""",
"""https://i.imgur.com/5DAMMyy.jpg""",
"""https://i.imgur.com/GNy8GQQ.jpg""",
"""https://i.imgur.com/pZO7wu1.jpg""",
"""https://i.imgur.com/GNB0RNc.jpg""",
"""https://i.imgur.com/JObRQIv.jpg""",
"""https://i.imgur.com/SQPcp7O.jpg""",
"""https://i.imgur.com/BMWAUVy.jpg""",
"""https://i.imgur.com/P1ktcWu.jpg""",
"""https://i.imgur.com/g4tWNME.jpg""",
"""https://i.imgur.com/skv31rn.jpg""",
"""https://i.imgur.com/6X5joMA.jpg""",
"""https://i.imgur.com/3clqshE.jpg""",
"""https://i.imgur.com/qGIkFsh.jpg""",
"""https://i.imgur.com/IvpQ3ZY.jpg""",
"""https://i.imgur.com/BEUy1bo.jpg""",
"""https://i.imgur.com/gkYTQ8S.jpg""",
"""https://i.imgur.com/rukotod.jpg""",
"""https://i.imgur.com/h38fKoZ.jpg""",
"""https://i.imgur.com/inX5Kpa.jpg""",
"""https://i.imgur.com/6lbvdvv.jpg""",
"""https://i.imgur.com/7eBj2kL.jpg""",
"""https://i.imgur.com/GPszjgW.jpg""",
"""https://i.imgur.com/Uka3X9i.jpg""",
"""https://i.imgur.com/YHy77bd.jpg""",
"""https://i.imgur.com/QBjXi91.jpg""",
"""https://i.imgur.com/VnE3UyK.jpg""",
"""https://i.imgur.com/vfVP6J8.jpg""",
"""https://i.imgur.com/rHXfBFb.jpg""",
"""https://i.imgur.com/v8HcoEN.jpg""",
"""https://i.imgur.com/6mLSPdf.jpg""",
"""https://i.imgur.com/b3qvYYO.jpg""",
"""https://i.imgur.com/YlRyWcg.jpg""",
"""https://i.imgur.com/RWvgMqD.jpg""",
"""https://i.imgur.com/6aa44eE.jpg""",
"""https://i.imgur.com/TAFJQpC.jpg""",
"""https://i.imgur.com/3LTGoYc.jpg""",
"""https://i.imgur.com/qabXrFy.jpg""",
"""https://i.imgur.com/rww9vEc.jpg""",
"""https://i.imgur.com/63RLFzq.jpg""",
"""https://i.imgur.com/nJUNzAK.jpg""",
"""https://i.imgur.com/mAobuVu.jpg""",
"""https://i.imgur.com/SQOGbf7.jpg""",
"""https://i.imgur.com/U54f3NX.jpg""",
"""https://i.imgur.com/XTlMhYw.jpg""",
"""https://i.imgur.com/pz7qjPL.jpg""",
"""https://i.imgur.com/I3Vx5oM.jpg""",
"""https://i.imgur.com/hdShHDC.jpg""",
"""https://i.imgur.com/p2AMLrL.jpg""",
"""https://i.imgur.com/X3jHPM3.jpg""",
"""https://i.imgur.com/pdrsFuz.jpg""",
"""https://i.imgur.com/fHzqgpt.jpg""",
"""https://i.imgur.com/UyQksrH.jpg""",
"""https://i.imgur.com/DvDXWpU.jpg""",
"""https://i.imgur.com/xvhPhQ5.jpg""",
"""https://i.imgur.com/0HnChG2.jpg""",
"""https://i.imgur.com/vS9QWrC.jpg""",
"""https://i.imgur.com/kTFhIW2.jpg""",
"""https://i.imgur.com/PfUCmhT.jpg""",
"""https://i.imgur.com/Bb2KY70.jpg""",
"""https://i.imgur.com/txt9ggu.jpg""",
"""https://i.imgur.com/O1DDHCI.jpg""",
"""https://i.imgur.com/B5o9nB2.jpg""",
"""https://i.imgur.com/EL90kjg.jpg""",
"""https://i.imgur.com/aF8D7MN.jpg""",
"""https://i.imgur.com/zGilSG6.jpg""",
"""https://i.imgur.com/sewVe6s.jpg""",
"""https://i.imgur.com/2FprdWS.jpg""",
"""https://i.imgur.com/a0d8X8V.jpg""",
"""https://i.imgur.com/UEUIh5N.jpg""",
"""https://i.imgur.com/RJUlZ46.jpg""",
"""https://i.imgur.com/VbScg3g.jpg""",
"""https://i.imgur.com/JhnCUMX.jpg""",
"""https://i.imgur.com/RZlH0IO.jpg""",
"""https://i.imgur.com/PcPCNd4.jpg""",
"""https://i.imgur.com/M8qeH9c.jpg""",
"""https://i.imgur.com/Xvahwfa.jpg""",
"""https://i.imgur.com/t0toVKv.jpg""",
"""https://i.imgur.com/HphuCSw.jpg""",
"""https://i.imgur.com/tzHUY0m.jpg""",
"""https://i.imgur.com/gDuqL4a.jpg""",
"""https://i.imgur.com/kLB6fH1.jpg""",
"""https://i.imgur.com/rhYTLXE.jpg""",
"""https://i.imgur.com/bwuOVIr.jpg""",
"""https://i.imgur.com/zrh6PpY.jpg""",
"""https://i.imgur.com/q0LpNdP.jpg""",
"""https://i.imgur.com/1dU7vUA.jpg""",
"""https://i.imgur.com/9li2NgJ.jpg""",
"""https://i.imgur.com/VRBqiTq.jpg""",
"""https://i.imgur.com/jNHD9OJ.jpg""",
"""https://i.imgur.com/w9rWgHK.jpg""",
"""https://i.imgur.com/2ss6TO0.jpg""",
"""https://i.imgur.com/6mLp3vA.jpg""",
"""https://i.imgur.com/I98Ux6S.jpg""",
"""https://i.imgur.com/ckftt7J.jpg""",
"""https://i.imgur.com/wT1zVy6.jpg""",
"""https://i.imgur.com/NV6dgBc.jpg""",
"""https://i.imgur.com/yCIlkXq.jpg""",
"""https://i.imgur.com/9fC7LSE.jpg""",
"""https://i.imgur.com/XWKwBoz.jpg""",
"""https://i.imgur.com/wQ3sYL4.jpg""",
"""https://i.imgur.com/XeucHTs.jpg""",
"""https://i.imgur.com/ME8hsXu.jpg""",
"""https://i.imgur.com/jrLoOfS.jpg""",
"""https://i.imgur.com/gTT2ELQ.jpg""", 
]

GLASSES_SHAPES = ['Rectangle', 'D-Frame', 'Oval', 'Round', 'Browline', 'Aviator', 'Square']

FACE_CLF = RandomForestClassifier()


# FUNCTION 1:
def extract_face_features(face_cols):
    face_columns = []
    
    face_example = call_face_api("""http://blog.myeyewear2go.com/wp-content/uploads/2013/09/smart-people-in-glasses-img-11.jpg""")
    
    closing_qts = []
    
    for i in range(len(face_example)):
        char = face_example[i]

        if char == '"' and i not in closing_qts:
            col = ''

            j = i + 1

            new_char = face_example[j]

            while new_char != '"':
                col += new_char

                j += 1

                new_char = face_example[j]
            closing_qts.append(j)

            if len(col) > 1:
                face_columns.append(col)
                
    for i in range(len(face_columns)): 
        j = i

        while face_columns[j] != 'pupilLeft':
            face_columns.remove(face_columns[j])
        break
        
    for col in face_columns:
        colX = col + 'X'

        face_cols.append(colX)

        colY = col + 'Y'

        face_cols.append(colY)


# FUNCTION 2:
def create_face_df(num_imgs, face_cols):
    return pd.DataFrame(np.zeros(shape=(num_imgs,len(face_cols))), columns=face_cols)


# FUNCTION 3:
def populate_face_df(face_df, img_urls, start_row, extra_calls):
    row_num = start_row
    
    for url in img_urls[row_num:]:
        face_output = call_face_api(url)
        
        if face_output == '[]':
            for i in range(extra_calls):
                face_output = call_face_api(url)
                
                if face_output != '[]':
                    break
        
        col_num = 0
        
        for i in range(len(face_output)):
            char = face_output[i]
            
            if (char == 'x' or char == 'y') and face_output[i-1] == '"':
                num = ''
                
                num_index = i + 3
                
                digit = face_output[num_index]
                
                while digit not in ',{}' and num_index <= len(face_output)-1:
                    num += digit
                    
                    num_index += 1
                    
                    digit = face_output[num_index]
                face_df.iloc[row_num][col_num] = float(num)
                
                col_num += 1
        
        row_num += 1


# FUNCTION 4:
def drop_rows_reindex(face_df):
    drop_row_nums = []
    
    for i in range(len(face_df)):
        if face_df.iloc[i][0] == 0.0:
            drop_row_nums.append(i)
            
    clean_face_df = face_df.drop(drop_row_nums)
    
    clean_face_df.index = range(len(clean_face_df))
    
    return clean_face_df


# FUNCTION 5:
def add_target_column(face_df, glasses_shapes):
    
    target_vals = ['Rectangle',
                    'D-Frame',
                    'Oval',
                    'Aviator',
                    'Round',
                    'Rectangle',
                    'D-Frame',
                    'Rectangle',
                    'Aviator',
                    'Rectangle',
                    'Round',
                    'Oval',
                    'Rectangle',
                    'Rectangle',
                    'Oval',
                    'Rectangle',
                    'Oval',
                    'D-Frame',
                    'Rectangle',
                    'Oval',
                    'Rectangle',
                    'Oval',
                    'Rectangle',
                    'D-Frame',
                    'Browline',
                    'Oval',
                    'Browline',
                    'D-Frame',
                    'Browline',
                    'Round',
                    'Rectangle',
                    'Rectangle',
                    'Rectangle',
                    'Round',
                    'Browline',
                    'Oval',
                    'Rectangle',
                    'Oval',
                    'Oval',
                    'Rectangle', 
                    'Rectangle',
                    'Oval',
                    'Oval',
                    'Rectangle',
                    'D-Frame',
                    'Oval',
                    'Round',
                    'Rectangle',
                    'Oval',
                    'Rectangle',
                    'Oval',
                    'Rectangle',
                    'D-Frame',
                    'Square',
                    'Oval',
                    'Rectangle',
                    'Round',
                    'Rectangle',
                    'Rectangle',
                    'Browline',
                    'Rectangle',
                    'Rectangle',
                    'Rectangle',
                    'Oval',
                    'D-Frame',
                    'Browline',
                    'D-Frame',
                    'Rectangle']
    
    if len(target_vals) > len(face_df):
        diff = len(target_vals) - len(face_df)
        
        target_vals = target_vals[:-1 - (diff-1)]
        
    if len(target_vals) < len(face_df):
        diff = len(face_df) - len(target_vals)
        
        for i in range(diff):
            target_vals.append(secure_random.choice(glasses_shapes))
            
    face_df['glassesShape'] = pd.Series(target_vals, index=face_df.index)


# FUNCTION 6:
def train_model(face_df, face_clf):
    features = face_df.columns[:-1]

    y = pd.factorize(face_df['glassesShape'])[0]
    
    face_clf.fit(face_df[features], y)


# FUNCTION CALL 1:
extract_face_features(FACE_COLS)


# FUNCTION CALL 2:
FACE_DF = create_face_df(NUM_IMGS, FACE_COLS)


# FUNCTION CALL 3:
populate_face_df(FACE_DF, IMG_URLS, 0, 15)


# FUNCTION CALL 4:
FACE_DF = drop_rows_reindex(FACE_DF)


# FUNCTION CALL 5:
add_target_column(FACE_DF, GLASSES_SHAPES)


# FUNCTION CALL 6:
train_model(FACE_DF, FACE_CLF)


save = [FACE_COLS, FACE_DF, FACE_CLF]
with open("save.pickle", 'wb') as f:
    pickle.dump(save, f)