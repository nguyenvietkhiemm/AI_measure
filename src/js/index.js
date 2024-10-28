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
    encodeInput(inputDict) {
        const encodedInput = { ...inputDict };
        for (const [column, values] of Object.entries(columns_encoder)) {
            if (encodedInput.hasOwnProperty(column)) {
                const valueIndex = values.indexOf(encodedInput[column]);
                if (valueIndex !== -1) {
                    encodedInput[column] = valueIndex;
                }
            }
        }
        return encodedInput;
    }
    decodeOutput(outputDict) {
        const decodedOutput = { ...outputDict };
        for (const [column, values] of Object.entries(columns_encoder)) {
            if (decodedOutput.hasOwnProperty(column)) {
                const index = decodedOutput[column];
                decodedOutput[column] = values[index];
            }
        }
        return decodedOutput;
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
        inputDict = Object.keys(inputDict)
        .filter(key => this.input_columns.includes(key) && inputDict[key] !== "" && (typeof inputDict[key] === 'number' || (typeof inputDict[key] === 'string' && inputDict[key].trim() !== "")))
        .reduce((obj, key) => {
            obj[key] = inputDict[key];
            return obj;
        }, {});

        console.log(JSON.stringify(inputDict));
        const inputKeys = Object.keys(inputDict);            

        const encodedInputDict = this.encodeInput(inputDict);
        const input = this.input_columns.map(col => encodedInputDict[col]);
        const outputKeys = this.output_columns.filter(col => !Object.keys(inputDict).includes(col));
        
        const modelIndex = this.findModelIndex(encodedInputDict);
        const weights = this.models[modelIndex].w;
        const biases = this.models[modelIndex].b;

        const min_vals_input = this.input_columns.map(col => this.min_vals[this.all_columns.indexOf(col)]);
        const max_vals_input = this.input_columns.map(col => this.max_vals[this.all_columns.indexOf(col)]);
        const min_vals_output = outputKeys.map(col => this.min_vals[this.all_columns.indexOf(col)]);
        const max_vals_output = outputKeys.map(col => this.max_vals[this.all_columns.indexOf(col)]);

        const normalizedInput = this.normalize(input, min_vals_input, max_vals_input);
        let output = new Array(weights.length).fill(0);
        for (let i = 0; i < output.length; i++) {
            output[i] = biases[i];
            for (let j = 0; j < normalizedInput.length; j++) {
                output[i] += normalizedInput[j] * weights[i][j];
            }
        }
        output = this.denormalize(output, min_vals_output, max_vals_output);
        output = output.map(result => parseFloat(result.toFixed(1)));
        
        const outputDict = {};
        for (let i = 0; i < outputKeys.length; i++) {
            outputDict[outputKeys[i]] = output[i];
        }
        return this.decodeOutput(outputDict);
    }
}
export default Linear_Model;