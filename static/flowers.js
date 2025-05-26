document.addEventListener("DOMContentLoaded", function () {
    const flowerBox = document.getElementById("flowerBox");

    // Liczba roślin – renderowana dynamicznie
    const flowerCount = {{ plants|length }};

    for (let i = 0; i < flowerCount; i++) {
        const flower = document.createElement("div");
        flower.classList.add("flower");
        flowerBox.appendChild(flower);
    }
});
