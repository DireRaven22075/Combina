function goto(location = "home.html") {
    window.scrollTo(0, 0);
    window.location.href = location;
    return;
}
function filter(name) {
    const docs = document.body;
    var children = Array.from(docs.children);
    if (name == "All") {
        children.forEach((child) => {
            if (child.tagName.toUpperCase() == "DIV") {
                child.style.display = "block";
            }
        });
        return;
    }
    children.forEach((child) => {
        if (child.tagName.toUpperCase() == "DIV") {
            if (child.classList.contains(name)) {
                child.style.display = "block";
            } else {
                child.style.display = "none";
            }
        }
    });
}
var selectedTag = [];
function search(type) {
    return;
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