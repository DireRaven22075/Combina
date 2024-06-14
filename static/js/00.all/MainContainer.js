//#region Interaction
function filter(platform) {
    const all = document.getElementById("Main");
    for (let i = 0; i < all.children.length; i++) {
        const element = all.children[i];
        if (platform === "All") {
            element.style.display = "block";
            continue;
        }
        if (element.classList.contains(platform)) {
            element.style.display = "block";
        } else {
            element.style.display = "none";
        }
    }
}
document.addEventListener("DOMContentLoaded", function() {
    const all = document.getElementById("Main");
    for (let i = 0; i < all.children.length; i++) {
        const element = all.children[i];
        element.children[element.children.length - 1].innerHTML = element.children[element.children.length - 1].innerHTML.replace('|||', '<br>');
    }
});
//#endregion 

//#region ui-updates
function ui_navigation(platform) {
    const target = document.getElementById("Navigation");
    for (const child of target.children) {
        child.style.color = (platform == "All") ? "#000000" : "#FFFFFF";
        child.disabled = child.value == platform;
    }
    switch(platform) {
        case "All": target.style.background = "#f9f9f9"; break;
        case "Facebook": target.style.background = "#0052FF"; break;
        case "Instagram": target.style.backgroundImage = 'linear-gradient(to right, rgb(255, 0, 169), rgb(255, 139, 0))'; break;
        case "X": target.style.background = "#101010"; element.style.color = "#FFFFFF"; break;
        case "Discord": target.style.background = "#6900FF"; break;
        case "Reddit": target.style.background = "#FFA000"; break;
        case "Everytime": target.style.background = "#303030"; break;
        case "Youtube": target.style.background = "#FF1A00"; break;
    }
}
//#endregion