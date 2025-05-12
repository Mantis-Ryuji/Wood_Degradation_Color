import numpy as np
import csv
import itertools
import pandas as pd

def LabCH_reader(file_list: list):
    
    length = len(file_list)
    output = []
    
    for i in range(length):
        data = []
        with open(file_list[i], mode='r', encoding='shift_jis') as file:
            reader = csv.reader(file)
            for _ in itertools.islice(reader, 7):
                pass
            for row in reader:
                data.append(row[:5])
        data = np.array(data).astype(np.float32)
        output.append(data)
        
    output = np.concatenate(output, axis=0)
    C_star = np.sqrt(np.power(output[:, 3], 2) + np.power(output[:, 4], 2))
    H_degree = np.rad2deg(np.arctan2(output[:, 4], output[:, 3]))
    H_degree[H_degree < 0] += 360

    xmin = output[:, 0].min()
    ymin = output[:, 1].min()
    xmax = output[:, 0].max()
    ymax = output[:, 1].max()
    
    x = int(xmax - xmin + 1)
    y = int(ymax - ymin + 1)

    L_star = output[:, 2].reshape(x, y, 1)
    a_star = output[:, 3].reshape(x, y, 1)
    b_star = output[:, 4].reshape(x, y, 1)
    C_star = C_star.reshape(x, y, 1)
    H_degree = H_degree.reshape(x, y, 1)

    results = np.concatenate([L_star, a_star, b_star, C_star, H_degree], axis=2)
    
    return results

def RGB_reader(file_list: list):
    
    length = len(file_list)
    output = []
    
    for i in range(length):
        data = []
        with open(file_list[i], mode='r', encoding='shift_jis') as file:
            reader = csv.reader(file)
            for _ in itertools.islice(reader, 7):
                pass
            for row in reader:
                data.append(row[:5])
        data = np.array(data).astype(np.float32)
        output.append(data)
        
    output = np.concatenate(output, axis=0)

    xmin = output[:, 0].min()
    ymin = output[:, 1].min()
    xmax = output[:, 0].max()
    ymax = output[:, 1].max()
    
    x = int(xmax - xmin + 1)
    y = int(ymax - ymin + 1)

    R = output[:, 2].reshape(x, y, 1)
    G = output[:, 3].reshape(x, y, 1)
    B = output[:, 4].reshape(x, y, 1)

    results = np.concatenate([R, G, B], axis=2)
    
    return results


def spctr_reader(file_list: list):
    
    length = len(file_list)
    output = []
    
    for i in range(length):
        data = []
        with open(file_list[i], mode='r', encoding='shift_jis') as file:
            reader = csv.reader(file)
            for _ in itertools.islice(reader, 7):
                pass
            for row in reader:
                data.append(row[:2] + row[6:87])
        data = np.array(data).astype(np.float32)
        output.append(data)
        
    output = np.concatenate(output, axis=0)

    xmin = output[:, 0].min()
    ymin = output[:, 1].min()
    xmax = output[:, 0].max()
    ymax = output[:, 1].max()
    
    x = int(xmax - xmin + 1)
    y = int(ymax - ymin + 1)

    results = []

    for i in range(81):
        data = output[:, i+2].reshape(x, y)
        results.append(data)

    results = np.stack(results, axis=-1)
    
    return results

# Excel使う人用
def output_asExcel(data: np.ndarray, file_path: str):
    
    L_star = data[:, :, 0]
    a_star = data[:, :, 1]
    b_star = data[:, :, 2]
    C_star = data[:, :, 3]
    H_degree = data[:, :, 4]
    
    df_L_star = pd.DataFrame(L_star)
    df_a_star = pd.DataFrame(a_star)
    df_b_star = pd.DataFrame(b_star)
    df_C_star = pd.DataFrame(C_star)
    df_H_degree = pd.DataFrame(H_degree)
    
    dataframes = [df_L_star, df_a_star, df_b_star, df_C_star, df_H_degree]
    names = ['L_star', 'a_star', 'b_star', 'C_star', 'H_degree']
    
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for data, name in zip(dataframes, names):
            data.to_excel(writer, sheet_name=name, index=False, header=False)

    return f"Data has been successfully saved to {file_path}"