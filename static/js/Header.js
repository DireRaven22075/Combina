function switchColor(platform, element) {
    const target = document.getElementById("Header");
    switch(platform) {
        default: target.style.background = "#00FFA8"; break;
        case "Facebook": target.style.background = "#0052FF"; break;
        case "Instagram": target.style.backgroundImage = 'linear-gradient(to right, rgb(255, 0, 169), rgb(255, 139, 0))'; break;
        case "X": target.style.background = "#101010"; break;
        case "Discord": target.style.background = "#6900FF"; break;
        case "Reddit": target.style.background = "#FF4300"; break;
        case "Everytime": target.style.background = "#FFFFFF"; break;
        case "Youtube": target.style.background = "#E93E29"; break;
    }
}
function filter(element, platform) {
    const target = document.getElementById("Header");
    for (const child of target.children[1].children) {
        child.style.fontSize = "1em";
    }
    switch(platform) {
        case "All": target.style.background = "#00FFA8"; break;
        case "Facebook": target.style.background = "#0052FF"; break;
        case "Instagram": target.style.backgroundImage = 'linear-gradient(to right, rgb(255, 0, 169), rgb(255, 139, 0))'; break;
        case "X": target.style.background = "#101010"; break;
        case "Discord": target.style.background = "#6900FF"; break;
        case "Reddit": target.style.background = "#FF4300"; break;
        case "Everytime": target.style.background = "#FFFFFF"; break;
        case "Youtube": target.style.background = "#E93E29"; break;
    }
}