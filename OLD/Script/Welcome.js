window.onload = function() {
    var body = document.body;
    body.style.height = window.innerHeight + "px";
}
window.onscroll = function (ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        location.href = "./home.html";
        window.onload = window.scrollTo(0, 0);
    }
}