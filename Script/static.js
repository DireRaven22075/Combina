function goto(location = "home.html") {
    window.scrollTo(0, 0);
    window.location.href = location;
    return;
}
var selectedTag = [];
function search(type) {
    var docs = document.title.split(" : ")[1];
    var home = document.getElementById(docs);
    var children = Array.from(home.children);
    var title = document.getElementById("Title");
    if (type == "All") {
        children.forEach((child) => child.style.display = "block");
        switch (docs) {
            default: case "Home": title.innerHTML = "Home"; return;
            case "Index": title.innerHTML = "Combina"; return;
            case "Search": title.innerHTML = "All"; return;
        }
    }
    else {
        children.forEach((child) => child.style.display = child.classList.contains(type) ? "block" : "none");
        title.innerHTML = type;
        return;
    }
}

window.onload += function() {
    const lower = document.getElementById("lower");
}