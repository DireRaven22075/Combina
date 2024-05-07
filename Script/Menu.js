function login(name) {
    temp(name);
    return;
}
function showlist() {
    const body = document.getElementById("AccountList");
    const text = document.getElementsByClassName("add")[0].children[0];
    const image = document.getElementsByClassName("add")[0].children[0];
    if (body.style.display == "block") {
        body.style.display = "none";
        text.innerHTML = "창 닫기";
        image.style.display = "none";
        return;
    } else {
        body.style.display = "block";
        text.innerHTML = "계정 추가";
        image.style.display = "block";
        return;
    }
    body.style.display = (body.style.display == "block") ? "none" : "block";
}
function temp(name) {
    const body = document.getElementById(name);
    body.style.display = "block";

}