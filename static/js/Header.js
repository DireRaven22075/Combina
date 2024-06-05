function filter(element, platform) {
    const target = document.getElementById("Header");
    const logoBlack = document.getElementById("Logo_Black");
    const logoWhite = document.getElementById("Logo_White");
    const content = document.getElementById("Content");
    logoBlack.style.display = (platform == "All" || platform == "Everytime") ? "block": "none";
    logoWhite.style.display = logoBlack.style.display == "block" ? "none" : "block";
    for (const child of target.children[1].children) {
        child.style.color = (platform == "All" || platform == "Everytime") ? "#000000" : "#FFFFFF";
        child.disabled = child === element;
    }
    //Sync Header Background to current platform
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
    //Filter Content
    for (const child of content.children) {
        child.style.display = child.classList.contains(platform) || platform == "All" ? "block" : "none";
    }
    return;
}