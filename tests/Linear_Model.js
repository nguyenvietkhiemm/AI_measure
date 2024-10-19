const data = {
    "weights": [
        [
            0.00047030891921131683,
            -0.020623582904934733
        ],
        [
            -0.041325397034641366,
            0.40420680684219945
        ],
        [
            -0.03189764072920435,
            0.08501883722318312
        ],
        [
            0.03005608930132824,
            0.1069357421195712
        ],
        [
            0.015157244055773542,
            0.24966590209069386
        ],
        [
            0.03489764464851527,
            0.31287785023951564
        ],
        [
            -0.00896952377903367,
            0.14893746339197195
        ],
        [
            -0.04429390770441809,
            0.3224749502953394
        ],
        [
            -0.023531406776005674,
            0.17355921084675718
        ],
        [
            -0.02695299070439288,
            0.10163917501903529
        ],
        [
            -0.008945960874623446,
            0.16273750420180183
        ]
    ],
    "biases": [
        0.5578403907663815,
        0.21095366299386115,
        0.18470379163996492,
        0.2570326996196384,
        0.06918702979625659,
        0.10720543230695236,
        0.271745928127955,
        0.2351733948133568,
        0.1852892767125746,
        0.4022886726398032,
        0.39019505345745414
    ],
    "min_vals": [
        1.0,
        10.0,
        10.0,
        10.0,
        10.0,
        10.0,
        10.0,
        10.0,
        10.0,
        10.0,
        10.0,
        11.0,
        19.0
    ],
    "max_vals": [
        2.0,
        68.0,
        29.0,
        28.0,
        38.0,
        47.0,
        91.0,
        63.0,
        41.0,
        39.0,
        45.0,
        50.0,
        89.0
    ]
};
class Linear_Model {
    constructor() {
        const { weights, biases, min_vals, max_vals } = data;
        this.weights = weights;
        this.biases = biases;
        this.min_vals = min_vals;
        this.max_vals = max_vals;
    }

    // Hàm chuẩn hóa giá trị đầu vào
    normalize(input, min_vals, max_vals) {
        return input.map((value, i) => (value - min_vals[i]) / (max_vals[i] - min_vals[i]));
    }

    // Hàm đưa giá trị từ chuẩn hóa về gốc
    denormalize(normalizedInput, min_vals, max_vals) {
        return normalizedInput.map((value, i) => value * (max_vals[i] - min_vals[i]) + min_vals[i]);
    }

    // Hàm dự đoán giá trị đầu ra
    predict(input) {
        // Chia min_vals và max_vals thành cho đầu vào và đầu ra
        const min_vals_input = this.min_vals.slice(0, input.length);
        const max_vals_input = this.max_vals.slice(0, input.length);
        const min_vals_output = this.min_vals.slice(input.length);
        const max_vals_output = this.max_vals.slice(input.length);

        // Chuẩn hóa đầu vào
        input = this.normalize(input, min_vals_input, max_vals_input);
    
        let results = new Array(this.weights.length).fill(0);
    
        for (let i = 0; i < results.length; i++) {
            results[i] = this.biases[i];
            for (let j = 0; j < input.length; j++) {
                results[i] += input[j] * this.weights[i][j];
            }
        }

        // Chuẩn hóa ngược để đưa ra kết quả cuối cùng
        results = this.denormalize(results, min_vals_output, max_vals_output);
        results = results.map(result => parseFloat(result.toFixed(1)));
        return results;
    }
}

export default Linear_Model;