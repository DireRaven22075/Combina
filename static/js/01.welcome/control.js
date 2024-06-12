/* 웰컴 화면 내의 모든 화면 컨트롤을 담당하는 함수 */
function control(dest) {
    const btn = document.getElementById('Btn');
    const page = [document.getElementById('First'), document.getElementById('Second')];
    if (dest=='next') {
        if (page[0].style.display == 'flex') {
            page[0].style.display = 'none';
            page[1].style.display = 'flex';
            btn.value = "Continue";
        }
        else {
            window.location.href = '/home';
            window.scrollTo(0,0);
        }
    }
    else {
        if (page[1].style.display == 'flex') {
            page[1].style.display = 'none';
            page[0].style.display = 'flex';
            btn.value = "Get Started...";
        }
    }
    return;
}