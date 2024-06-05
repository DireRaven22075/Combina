function setColorById(platform, id) {
    const target = document.getElementById(id);
    switch(platform) {
        case "All": target.style.background = "#FFFFFF"; break;
        case "Facebook": target.style.background = "#0052FF"; break;
        case "Instagram": target.style.backgroundImage = 'linear-gradient(to right, rgb(255, 0, 169), rgb(255, 139, 0))'; break;
        case "X": target.style.background = "#101010"; element.style.color = "#FFFFFF"; break;
        case "Discord": target.style.background = "#6900FF"; break;
        case "Reddit": target.style.background = "#FF4300"; break;
        case "Everytime": target.style.background = "#FFFFFF"; break;
        case "Youtube": target.style.background = "#E93E29"; break;
    }
}