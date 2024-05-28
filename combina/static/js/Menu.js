function closePopUp() {
    const id = document.getElementById("PopUp");
    id.style.display = "none";
}
document.addEventListener("click", function (e) {
    const id = document.getElementById("PopUp");
    if (id.style.display === "block" && e.target === id) {
        id.style.display = "none";
    }
});
window.onload += () => {
    const id = document.getElementById("PopUp");
    id.style.display = "none";
};
function disconnect(json) {
    const id = document.getElementById("PopUp");
    id.style.display = "block";
    const text = document.getElementById("PopUp_Text");
    text.innerHTML = json["name"] + "-" + json["platform"];
    text.innerHTML += "<br/>" + json["tag"];
}
function connect(json) {

}
function post(event) {
    if (event.target.tagName !== 'FORM') {
        event.target.closest('form').submit();
    } else {
        event.target.submit();
    }
}