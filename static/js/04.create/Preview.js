const preview = {
};
document.addEventListener("DOMContentLoaded", function() {
    preview['title'] = document.getElementById('PreviewTitle');
    preview['content'] = document.getElementById('PreviewContent');
    preview['image'] = document.getElementById('PreviewImage');
    document.getElementById('PostTitle').addEventListener('focusout', function (e) {
        preview['title'].innerHTML = e.target.value;
    });
    document.getElementById('PostContent').addEventListener('focusout', function (e) {
        preview['content'].innerHTML = e.target.value;
    });
    document.getElementById('PostImage').addEventListener('change', function (e) {
        var files = e.target.files;
        preview["image"].innerHTML = "";
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            var reader = new FileReader();
            reader.onload = function (e) {
                var img = document.createElement('img');
                img.src = e.target.result;
                preview["image"].appendChild(img);
            }
            reader.readAsDataURL(file);
        }
    });
});