import Linear_Model from "./Linear_Model.js";

document.addEventListener("DOMContentLoaded", () => {
    const linear_model = new Linear_Model();
    const inputs = document.querySelectorAll("#inputForm input, #inputForm select");

    inputs.forEach(input => {
        input.addEventListener("keyup", handleEvent);
        input.addEventListener("change", handleEvent);
    });

    function handleEvent(event) {
        event.preventDefault();

        const height = parseFloat(document.getElementById("height").value);
        const weight = parseFloat(document.getElementById("weight").value);
        const gender = parseInt(document.getElementById("gender").value);
        const age = parseInt(document.getElementById("age").value);
        const formValue = parseInt(document.getElementById("form").value);

        const shoulder = document.getElementById("shoulder").value ? parseFloat(document.getElementById("shoulder").value) : null;
        const sleeve = document.getElementById("sleeve").value ? parseFloat(document.getElementById("sleeve").value) : null;
        const neck = document.getElementById("neck").value ? parseFloat(document.getElementById("neck").value) : null;
        const chest = document.getElementById("chest").value ? parseFloat(document.getElementById("chest").value) : null;
        const waist = document.getElementById("waist").value ? parseFloat(document.getElementById("waist").value) : null;
        const stomach = document.getElementById("stomach").value ? parseFloat(document.getElementById("stomach").value) : null;
        const hip = document.getElementById("hip").value ? parseFloat(document.getElementById("hip").value) : null;
        const front_jacket = document.getElementById("front_jacket").value ? parseFloat(document.getElementById("front_jacket").value) : null;
        const biceps = document.getElementById("biceps").value ? parseFloat(document.getElementById("biceps").value) : null;
        const armhole = document.getElementById("armhole").value ? parseFloat(document.getElementById("armhole").value) : null;
        const front_vest = document.getElementById("front_vest").value ? parseFloat(document.getElementById("front_vest").value) : null;
        const back_length = document.getElementById("back_length").value ? parseFloat(document.getElementById("back_length").value) : null;

        const inputData = {
            height: height,
            weight: weight,
            age: age,
            gender: gender,
            form: formValue,
        };

        if (shoulder !== null) inputData.shoulder = shoulder;
        if (sleeve !== null) inputData.sleeve = sleeve;
        if (neck !== null) inputData.neck = neck;
        if (chest !== null) inputData.chest = chest;
        if (waist !== null) inputData.waist = waist;
        if (stomach !== null) inputData.stomach = stomach;
        if (hip !== null) inputData.hip = hip;
        if (front_jacket !== null) inputData.front_jacket = front_jacket;
        if (biceps !== null) inputData.biceps = biceps;
        if (armhole !== null) inputData.armhole = armhole;
        if (front_vest !== null) inputData.front_vest = front_vest;
        if (back_length !== null) inputData.back_length = back_length;

        const res = linear_model.predict(inputData);

        document.getElementById("shoulder").placeholder = res.shoulder || "";
        document.getElementById("sleeve").placeholder = res.sleeve || "";
        document.getElementById("neck").placeholder = res.neck || "";
        document.getElementById("chest").placeholder = res.chest || "";
        document.getElementById("waist").placeholder = res.waist || "";
        document.getElementById("stomach").placeholder = res.stomach || "";
        document.getElementById("hip").placeholder = res.hip || "";
        document.getElementById("front_jacket").placeholder = res.front_jacket || "";
        document.getElementById("biceps").placeholder = res.biceps || "";
        document.getElementById("armhole").placeholder = res.armhole || "";
        document.getElementById("front_vest").placeholder = res.front_vest || "";
        document.getElementById("back_length").placeholder = res.back_length || "";
    }
});
