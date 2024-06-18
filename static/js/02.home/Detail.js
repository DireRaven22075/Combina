//#region OnDocument Load
const Detail = {};
document.addEventListener("DOMContentLoaded", function () {
    Detail['name'] = document.getElementById('DetailUser');
    Detail['platform'] = document.getElementById('DetailPlatform');
    Detail['content'] = document.getElementById('DetailContent');
    Detail['image'] = document.getElementById('DetailImage');
    Detail['images'] = document.getElementById('DetailImages');
    Detail['video'] = document.getElementById('DetailVideo');
    Detail['button'] = document.getElementById('Redirect');
});
//#endregion
//#region Interaction
function setDetail(element) {
    Detail['platform'].innerHTML = element.children[0].value;
    Detail['name'].innerHTML = element.children[1].value;
    Detail['content'].innerHTML = element.children[2].innerHTML.replace('|||', '<br>');
    Detail['images'].innerHTML = "";
    Detail['video'].style.display = 'none';
    if (element.children.length > 5) {
        if (Detail['platform'].innerHTML == 'Youtube') {
            Detail['video'].style.display = 'block';
            Detail['video'].src = element.children[3].value;
        }
        else {
            for (var i = 4; i < element.children.length; i++) {
                var src = element.children[i].value;
                var img = document.createElement('img');
                img.classList.add('detail-image');
                img.src = src;
                Detail['images'].appendChild(img);
            }
        }
    }
    return;
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
    document.getElementById("Subtitle").style.visibility = "visible";
}
function closeDetail() {
    document.getElementById("Sub").style.visibility = "hidden";
    document.getElementById("Subtitle").style.visibility = "hidden";
}
//#endregion

//#region 

//#endregion