//#region OnDocument Load
const Detail = {};
document.addEventListener("DOMContentLoaded", function() {
    Detail['name'] = document.getElementById('DetailUser');
    Detail['platform'] = document.getElementById('DetailPlatform');
    Detail['content'] = document.getElementById('DetailContent');
    Detail['image'] = document.getElementById('DetailImage');
    Detail['images'] = document.getElementById('DetailImages');
    Detail['video'] = document.getElementById('DetailVideo');
});
//#endregion
//#region Interaction
function setDetail(element) {
    document.getElementById('DetailUser').innerHTML = element.children[0].children[0].children[0];
    document.getElementById('DetailPlatform').innerHTML = element.children[0].children[0].children[1].innerHTML;
    document.getElementById('DetailContent').innerHTML = element.children[0].children[1].children[0].innerHTML;
    document.getElementById('DetailImage').src = element.children[0].children[1].children[1].src;
    document.getElementById('DetailVideo').src = element.children[0].children[1].children[2].src;
}
function clearDetail() {
    Detail['name'].innerHTML = "";
    Detail['platform'].innerHTML = "";
    Detail['content'].innerHTML = "";
    Detail['image'].src = "";
    Detail['video'].src = "";
}
function openDetail() {
    document.getElementById("Sub").style.visibility = "visible";
    document.getElementById("SubTitle").style.visibility = "visible";
}
function closeDetail() {
    document.getElementById("Sub").style.visibility = "hidden";
    document.getElementById("SubTitle").style.visibility
}
//#endregion

//#region 

//#endregion