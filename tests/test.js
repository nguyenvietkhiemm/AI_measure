import Linear_Model from "./Linear_Model.js";

const linear_model = new Linear_Model();
let res = linear_model.predict([180, 70, 1, 25, 3]);

console.log(res);