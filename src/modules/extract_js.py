import json
from pathlib import Path

def extract_js(json_model_path, model, min_max_scaler):
    # Lấy các trọng số (coefficients) và bias (intercept)
    coefficients = model.coef_
    intercept = model.intercept_
    min_vals = min_max_scaler.data_min_
    max_vals = min_max_scaler.data_max_

    # Tạo một dictionary để lưu các trọng số và bias
    model_params = {
        'weights': coefficients.tolist(),
        'biases': intercept.tolist(),
        'min_vals': min_vals.tolist(),
        'max_vals': max_vals.tolist()
    }

        # Đọc nội dung của file gốc index.js
    with open(Path(r"js/index.js"), 'r', encoding='utf-8') as file:
        original_js_content = file.read()
    
    model_params_json = "const data = " + json.dumps(model_params, indent=4) + ";\n"
    
    new_js_content = model_params_json + original_js_content

    with open("{}\Linear_Model.js".format(json_model_path), 'w', encoding='utf-8') as json_file:
        json_file.write(new_js_content)

    print("Saved the model into {}\Linear_Model.json".format(json_model_path))
    


