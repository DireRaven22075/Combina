function filter(platform) {
    const area = document.getElementById('Main').children;
    for (var i = 0; i < area.length; i++) {
        const element = area[i];
        if (platform == 'All') {
            element.style.display = 'block';
            continue;
        }
        if (element.classList.contains(platform)) {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
    }
}