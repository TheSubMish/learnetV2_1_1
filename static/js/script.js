//navbar animation
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const chapMenu = document.querySelector(".chap-menu");

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
    chapMenu.classList.toggle("active");
});

document.querySelectorAll(".nav-link").forEach(n => n.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
}));

document.querySelectorAll(".chap-link").forEach(n => n.addEventListener("click", () => {
    hamburger.classList.remove("active");
    chapMenu.classList.remove("active");
}));

// Show glass card and hide
function hideDelete() {
    document.querySelector('.glass-card').style.display = 'none';
}

function showDelete() {
    document.querySelector('.glass-card').style.display = 'block';
}

//change background of checked category

const preCategories = document.querySelectorAll('.categories p');

preCategories.forEach(category => {
    const labels = category.querySelector('label');
    const input = category.querySelector('input');
    if(input.checked == true){
        category.style.backgroundColor = '#b27fff';
    }
    category.addEventListener("click", (event) => {
        if (event.target === labels) {
            const currentColor = window.getComputedStyle(category).getPropertyValue('background-color');
            console.log(currentColor);
            if (currentColor === 'rgb(178, 127, 255)') {
                category.style.backgroundColor = '#bfa0ed';
            } 
            if (currentColor === 'rgb(191, 160, 237)') {
                category.style.backgroundColor = '#b27fff';
            }
        }
    });
});


// profile picture of user
const profile = document.querySelector('.profile-picture-field input');
profile.addEventListener('change', () => {
    const picture = profile.files[0];
    const change = document.querySelector('.profile-picture');

    if (picture) {
        const imageUrl = URL.createObjectURL(picture);
        change.src = imageUrl
    }
});