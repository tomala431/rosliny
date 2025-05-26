document.addEventListener("DOMContentLoaded", function () {
    const flowerBox = document.getElementById("flowerBox");

    for (let i = 0; i < plantCount; i++) {
        const flower = document.createElement("div");
        flower.classList.add("flower");
        flowerBox.appendChild(flower);
    }
});
