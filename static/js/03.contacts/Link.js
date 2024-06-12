function Link(platform) {
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
    const target = document.getElementById("Navigation");
    for (const child of target.children) {
        child.style.color = (platform == "All") ? "#000000" : "#FFFFFF";
        child.disabled = child.value == platform;
    }
}