window.onload = function() {
    scrollTo(0, 0);
};
var selectedTag = [];
function filter(tag) {
    const home = document.getElementById("Home");
    const children = Array.from(home.children);
    if (tag == "All") {
        
    }
}
function search(type) {
    var home = document.getElementById("Home");
    var children = Array.from(home.children);
    children.forEach(function(child) {
        if (child.classList.contains(type)) {
            child.style.display = "block";
        } else {
            if (child.classList.contains())
            child.style.display = "none";
        }
    });
}
function unselect() {
    var home = document.getElementById("Home");
    var children = Array.from(home.children);
    children.forEach(function(child) {
        child.style.display = "block";
        console.log(child.classList);
    });
    console.log("Unselected");

};