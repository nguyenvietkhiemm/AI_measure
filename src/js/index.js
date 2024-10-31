class Linear_Model {
    constructor() {
        this.models = models;
        const { min_vals, max_vals } = min_max_vals;
        this.min_vals = min_vals;
        this.max_vals = max_vals;
        this.min = min;
        this.max = max;
        this.input_columns = input_columns;
        this.output_columns = output_columns;
        this.all_columns = all_columns;
    }
    oneHotEncodeInput(inputDict) {
        const oneHotDict = { ...inputDict };
        for (const [column, values] of Object.entries(encode)) {
            const value = inputDict[column];
            
            if (value) {
                values.forEach(col => {
                    oneHotDict[col] = 0;
                });
                const oneHotColumn = `${column}_${value}`;
                if (values.includes(oneHotColumn)) {
                    oneHotDict[oneHotColumn] = 1;
                }
            }
            delete oneHotDict[column];
        }
        return oneHotDict;
    }

    normalize(input, min_vals, max_vals) {
        return input.map((value, i) => ((value - min_vals[i]) / (max_vals[i] - min_vals[i])) * (this.max - this.min) + this.min);
    }

    denormalize(normalizedInput, min_vals, max_vals) {
        return normalizedInput.map((value, i) => {
            const range = max_vals[i] - min_vals[i];
            if (range === 0) return min_vals[i];
            return value * range / (this.max - this.min) + min_vals[i];
        });
    }

    findModelIndex(inputDict) {
        const binaryString = this.output_columns.map(col => (inputDict.hasOwnProperty(col) ? '1' : '0')).join('');
        return parseInt(binaryString, 2);
    }

    predict(inputDict) {
        inputDict = Object.keys(inputDict)
        .filter(key => 
            (this.all_columns.includes(key) || Object.keys(encode).includes(key)) &&inputDict[key] !== "" && (typeof inputDict[key] === 'number' || (typeof inputDict[key] === 'string' && inputDict[key].trim() !== "")))
        .reduce((obj, key) => {
            obj[key] = inputDict[key];
            return obj;
        }, {});
        console.log("================================");
        console.log(`Input before processing:`, JSON.stringify(inputDict));    
        inputDict = this.oneHotEncodeInput(inputDict);
        inputDict = this.all_columns.reduce((sortedObj, col) => {
            if (inputDict.hasOwnProperty(col)) {
                sortedObj[col] = inputDict[col];
            }
            return sortedObj;
        }, {});
        const inputKeys = Object.keys(inputDict);
        const outputKeys = this.output_columns.filter(col => !inputKeys.includes(col));

        if (inputKeys.length < this.input_columns.length){
            console.error("Not enough input data to predict.");
            return {};
        }
        const modelIndex = this.findModelIndex(inputDict);
        
        console.log(`[${modelIndex}] Input after processing:`, JSON.stringify(inputDict));

        const weights = this.models[modelIndex].w;
        const biases = this.models[modelIndex].b;

        const min_vals_input = inputKeys.map(col => this.min_vals[this.all_columns.indexOf(col)]);
        const max_vals_input = inputKeys.map(col => this.max_vals[this.all_columns.indexOf(col)]);
        const min_vals_output = outputKeys.map(col => this.min_vals[this.all_columns.indexOf(col)]);
        const max_vals_output = outputKeys.map(col => this.max_vals[this.all_columns.indexOf(col)]);

        const normalizedInput = this.normalize(Object.values(inputDict), min_vals_input, max_vals_input);
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
        
        return outputDict;
    }
}

export default Linear_Model;