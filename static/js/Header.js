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
    const logoBlack = document.getElementById("Logo_Black");
    const logoWhite = document.getElementById("Logo_White");
    for (const child of target.children[1].children) {
        switch(platform) {
            case "All": case "Everytime": 
                child.style.color = "#000000";
                logoBlack.style.display = "block";
                logoWhite.style.display = "none";
                break;
            default:
                child.style.color = "#FFFFFF";
                logoBlack.style.display = "none";
                logoWhite.style.display = "block";
                break;
        }
        if (child === element) {
            child.disabled = true;
        }
        else {
            child.disabled = false;
        }
    }
    switch(platform) {
        case "All": target.style.background = "#FFFFFF"; break;
        case "Facebook": target.style.background = "#0052FF"; 
            element.style.color = "#FFFFFF";
            break;
        case "Instagram":
            target.style.backgroundImage = 'linear-gradient(to right, rgb(255, 0, 169), rgb(255, 139, 0))';
            element.style.color = "#FFFFFF";
            break;
        case "X":
            target.style.background = "#101010";
            element.style.color = "#FFFFFF";
            break;
        case "Discord": 
            target.style.background = "#6900FF";
            element.style.color = "#FFFFFF";
            break;
        case "Reddit":
            target.style.background = "#FF4300";
            element.style.color = "#FFFFFF";
            break;
        case "Everytime":
            target.style.background = "#FFFFFF";
            element.color
            break;
        case "Youtube": target.style.background = "#E93E29"; break;
    }
}