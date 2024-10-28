import requests
import json
import csv
import re
import numpy as np

def inch_to_cm(number):
    return round(float(number) * 2.54, 2)

def parse_value_with_unit(value):
    if isinstance(value, (int, float)):
        return value
    match = re.match(r"([0-9.]+)([a-zA-Z]*)", value)
    if match:
        number = match.group(1)
        unit = match.group(2)
        if unit == 'inch':
            return inch_to_cm(number)
        return float(number)
    return value

def parse_value(value, default=np.nan):
    if value is None or value == '' or value == np.nan:
        return default
    return value

def get_api_data_post(url, data, dataset_csv, input_columns, output_columns):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print("RESPONSE STATUS:", response)
    columns = input_columns + output_columns
    def parse_measurement_data(data):
        result = {}
        for key, entry in data.items():
            result[key] = {k : np.nan for k in columns}
            info = entry['information']
            result[key].update({
                k: parse_value(info.get(k, np.nan)) for k in input_columns
            })
            measurements = list(entry['measurements_infor'])
            if isinstance(measurements, list):
                for measurement in measurements:
                    if isinstance(measurement, dict):
                        name = measurement.get('name')
                        value = parse_value(measurement.get('value', np.nan))
                        unit = measurement.get('unit', np.nan)
                        
                        if name in columns:
                            if unit == 'inch' and value != np.nan:
                                try:
                                    value_in_cm = inch_to_cm(value)
                                    value = value_in_cm
                                except ValueError:
                                    print(f"Error converting {name}: {value} inch\n")
                            result[key][name] = value
        return result
    parsed_data = json.loads(response.text.replace('\\n', '').replace('\\r', ''))
    res = parse_measurement_data(parsed_data)
    with open(dataset_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for id, measurements in res.items():
            row = {}
            row.update(measurements)
            
            for key, value in measurements.items():
                row[key] = parse_value_with_unit(value)
            writer.writerow(row)
        print("saved dataset in ", dataset_csv)