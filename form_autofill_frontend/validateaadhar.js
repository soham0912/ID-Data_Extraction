async function checkImage() {

    const image1 = document.getElementById('image1');
    const imageStatusMessage = document.getElementById("imageStatusMessage");
    const file1 = image1.files[0];
    const formData = new FormData();
    formData.append("image", file1);

    const response = await fetch('http://localhost:5000/detect-aadhar-front', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    
    if (data.Aadhar == "Yes" && data.Front == "Yes") {
        imageStatusMessage.textContent = "";
        localStorage.setItem("aadharDetailsfront", JSON.stringify(data));
        return true;
    } else if (data.Aadhar == "Yes" && data.Front == "No") {
        imageStatusMessage.textContent = "Kindly upload your front side of Aadhar here!";
    } else {
        imageStatusMessage.textContent = "Invalid Aadhar uploaded!";
    }

    return false;
}

async function checkImage2() {

    const image2 = document.getElementById('image2');
    const imageStatusMessage2 = document.getElementById("imageStatusMessage2");
    const file2 = image2.files[0];
    const formData = new FormData();
    formData.append("image", file2);

    const response = await fetch('http://localhost:4200/detect-aadhar-back', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();

    if (data.Aadhar == "Yes" && data.Back == "Yes") {
        imageStatusMessage2.textContent = "";
        localStorage.setItem("aadharDetailsback", JSON.stringify(data));
        return true;
    } else if (data.Aadhar == "Yes" && data.Back == "No") {
        imageStatusMessage2.textContent = "Kindly upload your back side of Aadhar here!";
    } else {
        imageStatusMessage2.textContent = "Invalid Aadhar uploaded!";
    }

    return false;
}

async function redirect() {
    const [isImage1Valid, isImage2Valid] = await Promise.all([checkImage(), checkImage2()]);

    if (isImage1Valid && isImage2Valid) {
        window.location.href = "form.html";
    }

}

function validateAadhar() {
    redirect();
}