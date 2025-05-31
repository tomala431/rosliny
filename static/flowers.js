document.addEventListener("DOMContentLoaded", function () {
    const flowerBox = document.getElementById("flowerBox");

    // Tablica dostępnych obrazków kwiatków
    const flowerImages = [
        '/static/icons/flower1.gif',
        '/static/icons/flower2.gif',
        '/static/icons/flower3.gif'
    ];

    for (let i = 0; i < plantCount; i++) {
        const flower = document.createElement("div");
        flower.classList.add("flower");

        // Losowy wybór obrazka
        const randomIndex = Math.floor(Math.random() * flowerImages.length);
        const selectedImage = flowerImages[randomIndex];

        // Ustawiamy tło na losowy obrazek
        flower.style.backgroundImage = `url('${selectedImage}')`;

        flowerBox.appendChild(flower);
    }
});
