const preview = {
};
document.addEventListener("DOMContentLoaded", function() {
    preview['title'] = document.getElementById('PreviewTitle');
    preview['content'] = document.getElementById('PreviewContent');
    preview['image'] = document.getElementById('PreviewImage');
    preview['images'] = document.getElementById('PreviewImages');
    document.getElementById('PostTitle').addEventListener('focusout', function (e) {
        preview['title'].innerHTML = e.target.value;
    });
    document.getElementById('PostContent').addEventListener('focusout', function (e) {
        preview['content'].innerHTML = e.target.value;
    });
    document.getElementById('PostImage').addEventListener('change', function (e) {
        var files = e.target.files;
        preview["images"].innerHTML = "";
        preview['image'].innerHTML = "";
        if (files.length == 0) return;
        if (files.length == 1) {
            var file = files[0];
            var reader = new FileReader();
            reader.onload = function (e) {
                var img = document.createElement('img');
                img.classList.add('prevent-overflow');
                img.src = e.target.result;
                preview["image"].appendChild(img);
            }
            reader.readAsDataURL(file);
            return; 
        }
        var size = files.length > 4 ? 4 : files.length;
        for (var i = 0; i < size; i++) {
            var file = files[i];
            var reader = new FileReader();
            reader.onload = function (e) {
                var img = document.createElement('img');
                img.classList.add('prevent-overflow');
                img.src = e.target.result;
                preview["images"].appendChild(img);
            }
            reader.readAsDataURL(file);
        }
    });
});