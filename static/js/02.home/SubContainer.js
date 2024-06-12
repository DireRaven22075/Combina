//#region Interaction
function openDetail(element) {
    const value = element.children[0].value;
    const content = document.getElementById("Sub");
    const title = document.getElementById("Subtitle");
    content.style.display = "block";
    title.style.display = "block";
}
function closeDetail() {
    const content = document.getElementById("Sub");
    const title = document.getElementById("Subtitle");
    
    content.style.display = "none";
    title.style.display = "none";
}
//#endregion

//#region 

//#endregion