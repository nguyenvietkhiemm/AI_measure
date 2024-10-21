class Linear_Model {
    constructor() {
        this.models = models;
        const { min, max } = min_max_vals;
        this.min_vals = min;
        this.max_vals = max;
        this.input_columns = input_columns;
        this.output_columns = output_columns;
        this.all_columns = input_columns.concat(output_columns);
    }
    normalize(input, min_vals, max_vals) {
        return input.map((value, i) => (value - min_vals[i]) / (max_vals[i] - min_vals[i]));
    }
    denormalize(normalizedInput, min_vals, max_vals) {
        return normalizedInput.map((value, i) => value * (max_vals[i] - min_vals[i]) + min_vals[i]);
    }
    findModelIndex(inputDict) {
        const binaryString = this.output_columns.map(col => (inputDict.hasOwnProperty(col) ? '1' : '0')).join('');
        return parseInt(binaryString, 2);
    }
    predict(inputDict) {
        const inputKeys = Object.keys(inputDict);
        const outputKeys = this.output_columns.filter(col => !inputKeys.includes(col));
        const input = inputKeys.map(key => inputDict[key]);
        console.log("INPUT", input);
        const modelIndex = this.findModelIndex(inputDict);
        const weights = this.models[modelIndex].w;
        const biases = this.models[modelIndex].b;

        const min_vals_input = inputKeys.map(col => this.min_vals[this.all_columns.indexOf(col)]);
        const max_vals_input = inputKeys.map(col => this.max_vals[this.all_columns.indexOf(col)]);
        const min_vals_output = outputKeys.map(col => this.min_vals[this.all_columns.indexOf(col)]);
        const max_vals_output = outputKeys.map(col => this.max_vals[this.all_columns.indexOf(col)]);

        console.log(min_vals_input);
        console.log(max_vals_input);
        console.log(outputKeys);

        const normalizedInput = this.normalize(input, min_vals_input, max_vals_input);
        let results = new Array(weights.length).fill(0);
        for (let i = 0; i < results.length; i++) {
            results[i] = biases[i];
            for (let j = 0; j < normalizedInput.length; j++) {
                results[i] += normalizedInput[j] * weights[i][j];
            }
        }
        results = this.denormalize(results, min_vals_output, max_vals_output);
        results = results.map(result => parseFloat(result.toFixed(1)));
        const outputDict = {};

        for (let i = 0; i < outputKeys.length; i++) {
            outputDict[outputKeys[i]] = results[i];
        }

        return outputDict;
    }
}
export default Linear_Model;