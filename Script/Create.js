function submit() {
    const title = document.getElementById("Title").value;
    const content = document.getElementById("Content").value;
    const files = document.getElementById("File").files;
    const data = {
        title: title,
        content: content,
    };
}