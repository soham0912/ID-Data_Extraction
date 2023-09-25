// Function to handle file input change and display images
function handleFileInputChange(fileInput, imageElement) {
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            imageElement.src = event.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        imageElement.src = "#"; // Clear the image if no file is selected
    }
}

// Get references to the file input elements and image elements
const fileInput1 = document.getElementById("image1");
const image1 = document.getElementById("img1");
const fileInput2 = document.getElementById("image2");
const image2 = document.getElementById("img2");

// Add event listeners to file inputs to handle changes and display images
fileInput1.addEventListener("change", function () {
    handleFileInputChange(fileInput1, image1);
});

fileInput2.addEventListener("change", function () {
    handleFileInputChange(fileInput2, image2);
});
