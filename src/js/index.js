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