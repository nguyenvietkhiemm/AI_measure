import Linear_Model from "./Linear_Model_no_split.js";

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
        const formValue = (document.getElementById("form").value);

        const shoulder = document.getElementById("shoulder").value ? parseFloat(document.getElementById("shoulder").value) : null;
        const sleeve = document.getElementById("sleeve").value ? parseFloat(document.getElementById("sleeve").value) : null;
        const long_sleeve = document.getElementById("long_sleeve").value ? parseFloat(document.getElementById("long_sleeve").value) : null;
        const neck = document.getElementById("neck").value ? parseFloat(document.getElementById("neck").value) : null;
        const chest = document.getElementById("chest").value ? parseFloat(document.getElementById("chest").value) : null;
        const waist = document.getElementById("waist").value ? parseFloat(document.getElementById("waist").value) : null;
        const stomach = document.getElementById("stomach").value ? parseFloat(document.getElementById("stomach").value) : null;
        const hip = document.getElementById("hip").value ? parseFloat(document.getElementById("hip").value) : null;
        const pants_length = document.getElementById("pants_length").value ? parseFloat(document.getElementById("pants_length").value) : null;
        const biceps = document.getElementById("biceps").value ? parseFloat(document.getElementById("biceps").value) : null;
        const armhole = document.getElementById("armhole").value ? parseFloat(document.getElementById("armhole").value) : null;
        const thight = document.getElementById("thight").value ? parseFloat(document.getElementById("thight").value) : null;
        const crotch = document.getElementById("crotch").value ? parseFloat(document.getElementById("crotch").value) : null;

        const inputData = {
            height: height,
            weight: weight,
            age: age,
            gender: gender,
            form: formValue,
        };

        console.log("INPUT: " + JSON.stringify(inputData));

        if (shoulder !== null) inputData.shoulder = shoulder;
        if (sleeve !== null) inputData.sleeve = sleeve;
        if (long_sleeve !== null) inputData.long_sleeve = long_sleeve;
        if (neck !== null) inputData.neck = neck;
        if (chest !== null) inputData.chest = chest;
        if (waist !== null) inputData.waist = waist;
        if (stomach !== null) inputData.stomach = stomach;
        if (hip !== null) inputData.hip = hip;
        if (pants_length !== null) inputData.pants_length = pants_length;
        if (biceps !== null) inputData.biceps = biceps;
        if (armhole !== null) inputData.armhole = armhole;
        if (thight !== null) inputData.thight = thight;
        if (crotch !== null) inputData.crotch = crotch;


        const res = linear_model.predict(inputData);

        document.getElementById("shoulder").placeholder = res.shoulder || "";
        document.getElementById("sleeve").placeholder = res.sleeve || "";
        document.getElementById("long_sleeve").placeholder = res.long_sleeve || "";
        document.getElementById("neck").placeholder = res.neck || "";
        document.getElementById("chest").placeholder = res.chest || "";
        document.getElementById("waist").placeholder = res.waist || "";
        document.getElementById("stomach").placeholder = res.stomach || "";
        document.getElementById("hip").placeholder = res.hip || "";
        document.getElementById("pants_length").placeholder = res.pants_length || "";
        document.getElementById("biceps").placeholder = res.biceps || "";
        document.getElementById("armhole").placeholder = res.armhole || "";
        document.getElementById("thight").placeholder = res.thight || "";
        document.getElementById("crotch").placeholder = res.crotch || "";

        console.log("OUTPUT: " + JSON.stringify(res));
    }
});
