import random
def calculate_waist(row):
    height = row['height']
    weight = row['weight']
    
    if height < 110:
        result = height * 0.25 + weight * 0.3
    elif 110 <= height < 120:
        result = height * 0.26 + weight * 0.3
    elif 120 <= height < 130:
        result = height * 0.27 + weight * 0.3
    elif 130 <= height < 140:
        result = height * 0.28 + weight * 0.3
    elif 140 <= height < 150:
        result = height * 0.29 + weight * 0.3
    elif 150 <= height < 160:
        result = height * 0.30 + weight * 0.3
    elif 160 <= height < 170:
        result = height * 0.31 + weight * 0.3
    elif 170 <= height < 180:
        result = height * 0.32 + weight * 0.3
    elif 180 <= height < 190:
        result = height * 0.33 + weight * 0.3
    elif 190 <= height <= 270:
        result = height * 0.34 + weight * 0.3
    else:
        result = None
    
    if result is None:
        print(height)
    result += random.uniform(-1, 1)
    return round(result, 1)

def calculate_stomach(row):
    height = row['height']
    weight = row['weight']
    
    if height < 110:
        result = height * 0.30 + weight * 0.3
    elif 110 <= height < 120:
        result = height * 0.31 + weight * 0.3
    elif 120 <= height < 130:
        result = height * 0.32 + weight * 0.3
    elif 130 <= height < 140:
        result = height * 0.33 + weight * 0.3
    elif 140 <= height < 150:
        result = height * 0.34 + weight * 0.3
    elif 150 <= height < 160:
        result = height * 0.35 + weight * 0.3
    elif 160 <= height < 170:
        result = height * 0.36 + weight * 0.3
    elif 170 <= height < 180:
        result = height * 0.37 + weight * 0.3
    elif 180 <= height < 190:
        result = height * 0.38 + weight * 0.3
    elif 190 <= height <= 270:
        result = height * 0.39 + weight * 0.3
    else:
        result = None 
        
    result += random.uniform(-1, 1)
    return round(result, 1)
    
def calculate_hip(row):
    height = row['height']
    weight = row['weight']
    
    if height < 110:
        result = height * 0.35 + weight * 0.4
    elif 110 <= height < 120:
        result = height * 0.36 + weight * 0.4
    elif 120 <= height < 130:
        result = height * 0.37 + weight * 0.4
    elif 130 <= height < 140:
        result = height * 0.38 + weight * 0.4
    elif 140 <= height < 150:
        result = height * 0.39 + weight * 0.4
    elif 150 <= height < 160:
        result = height * 0.40 + weight * 0.4
    elif 160 <= height < 170:
        result = height * 0.41 + weight * 0.4
    elif 170 <= height < 180:
        result = height * 0.42 + weight * 0.4
    elif 180 <= height < 190:
        result = height * 0.43 + weight * 0.4
    elif 190 <= height <= 270:
        result = height * 0.44 + weight * 0.4
    else:
        result = None
        
    result += random.uniform(-1, 1)
    return round(result, 1)
    
def calculate_front_jacket(row):
    height = row['height']
    weight = row['weight']
    
    if height < 110:
        result = height * 0.32 + weight * 0.1
    elif 110 <= height < 120:
        result = height * 0.33 + weight * 0.1
    elif 120 <= height < 130:
        result = height * 0.34 + weight * 0.1
    elif 130 <= height < 140:
        result = height * 0.35 + weight * 0.1
    elif 140 <= height < 150:
        result = height * 0.36 + weight * 0.1
    elif 150 <= height < 160:
        result = height * 0.37 + weight * 0.1
    elif 160 <= height < 170:
        result = height * 0.38 + weight * 0.1
    elif 170 <= height < 180:
        result = height * 0.39 + weight * 0.1
    elif 180 <= height < 190:
        result = height * 0.40 + weight * 0.1
    elif 190 <= height <= 270:
        result = height * 0.41 + weight * 0.1
    else:
        result = None
        
    result += random.uniform(-1, 1)
    return round(result, 1)
    
def calculate_biceps(row):
    height = row['height']
    weight = row['weight']
    
    if height < 110:
        result = height * 0.07 + weight * 0.2
    elif 110 <= height < 120:
        result = height * 0.06 + weight * 0.2
    elif 120 <= height < 130:
        result = height * 0.09 + weight * 0.2
    elif 130 <= height < 140:
        result = height * 0.10 + weight * 0.2
    elif 140 <= height < 150:
        result = height * 0.11 + weight * 0.2
    elif 150 <= height < 160:
        result = height * 0.12 + weight * 0.2
    elif 160 <= height < 170:
        result = height * 0.13 + weight * 0.2
    elif 170 <= height < 180:
        result = height * 0.14 + weight * 0.2
    elif 180 <= height < 190:
        result = height * 0.15 + weight * 0.2
    elif 190 <= height <= 270:
        result = height * 0.16 + weight * 0.2
    else:
        result = None 

    result += random.uniform(-1, 1)
    return round(result, 1)
    
def calculate_armhole(row):
    height = row['height']
    weight = row['weight']
    
    if height < 110:
        result = height * 0.12 + weight * 0.3
    elif 110 <= height < 120:
        result = height * 0.13 + weight * 0.3
    elif 120 <= height < 130:
        result = height * 0.14 + weight * 0.3
    elif 130 <= height < 140:
        result = height * 0.15 + weight * 0.3
    elif 140 <= height < 150:
        result = height * 0.16 + weight * 0.3
    elif 150 <= height < 160:
        result = height * 0.17 + weight * 0.3
    elif 160 <= height < 170:
        result = height * 0.18 + weight * 0.3
    elif 170 <= height < 180:
        result = height * 0.19 + weight * 0.3
    elif 180 <= height < 190:
        result = height * 0.20 + weight * 0.3
    elif 190 <= height <= 270:
        result = height * 0.21 + weight * 0.3
    else:
        result = None
        
    result += random.uniform(-1, 1)
    return round(result, 1)

def calculate_front_vest(row):
    height = row['height']
    weight = row['weight']
    
    if height < 110:
        result = height * 0.3 + weight * 0.06
    elif 110 <= height < 120:
        result = height * 0.31 + weight * 0.06
    elif 120 <= height < 130:
        result = height * 0.32 + weight * 0.06
    elif 130 <= height < 140:
        result = height * 0.33 + weight * 0.06
    elif 140 <= height < 150:
        result = height * 0.34 + weight * 0.06
    elif 150 <= height < 160:
        result = height * 0.35 + weight * 0.06
    elif 160 <= height < 170:
        result = height * 0.36 + weight * 0.06
    elif 170 <= height < 180:
        result = height * 0.37 + weight * 0.06
    elif 180 <= height < 190:
        result = height * 0.38 + weight * 0.06
    elif 190 <= height <= 270:
        result = height * 0.39 + weight * 0.06
    else:
        result = None
    
    result += random.uniform(-1, 1)
    return round(result, 1)
    
def calculate_back_length(row):
    height = row['height']
    weight = row['weight']
    
    if height < 110:
        result = height * 0.3 + weight * 0.2
    elif 110 <= height < 120:
        result = height * 0.31 + weight * 0.2
    elif 120 <= height < 130:
        result = height * 0.32 + weight * 0.2
    elif 130 <= height < 140:
        result = height * 0.33 + weight * 0.2
    elif 140 <= height < 150:
        result = height * 0.34 + weight * 0.2
    elif 150 <= height < 160:
        result = height * 0.35 + weight * 0.2
    elif 160 <= height < 170:
        result = height * 0.36 + weight * 0.2
    elif 170 <= height < 180:
        result = height * 0.37 + weight * 0.2
    elif 180 <= height < 190:
        result = height * 0.38 + weight * 0.2
    elif 190 <= height <= 270:
        result = height * 0.39 + weight * 0.2
    else:
        result = None 
        
    result += random.uniform(-1, 1)
    return round(result, 1)

def determine_body_shape(row):
    shoulder = row['shoulder']
    waist = row['waist']
    hip = row['hip']
    
    if shoulder / hip > 1.2:
        result = "inverted_triangle"
    elif hip / shoulder > 1.1 and waist / hip > 0.75:
        result = "pear" 
    elif shoulder / hip > 1.1 and waist / shoulder > 0.75:
        result = "apple"
    elif abs(shoulder - hip) < 0.1 * shoulder and waist / shoulder < 0.75:
        result = "hourglass"
    else:
        result = "rectangle"
        
    return result

def create_data(df):
    """
    This function creates a data directory if it does not exist,
    and saves the DataFrame as a CSV file in the data directory.
    
    OVERFITTING
    
    """
    df['waist'] = df.apply(calculate_waist, axis=1)
    df['stomach'] = df.apply(calculate_stomach, axis=1)
    df['hip'] = df.apply(calculate_hip, axis=1)
    df['front_jacket'] = df.apply(calculate_front_jacket, axis=1)
    df['biceps'] = df.apply(calculate_biceps, axis=1)
    df['armhole'] = df.apply(calculate_armhole, axis=1)
    df['front_vest'] = df.apply(calculate_front_vest, axis=1)
    df['back_length'] = df.apply(calculate_back_length, axis=1)
    df['form'] = df.apply(determine_body_shape, axis=1)
    return df