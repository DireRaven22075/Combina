//Main Container 내에 있는 플랫폼 별로 요소를 활성화/비활성화 하는 함수
function filter(platform) {
    //Main Container 변수화
    const parent = document.getElementById("Main");
    //만약 설정된 플랫폼이 "All" 일경우 모든 요소를 보여줌
    if (platform == "All") {
        //모든 요소에 대한 반복문 선언
        for(const child of parent.children)
            child.style.display = "block";
        //함수 종료
        return;
    }
    //설정된 플랫폼에 맞춰서 요소를 활성화 / 비활성화
    for(const child of parent.children)
        //모든 요소에 대한 반복문 선언
        child.style.display = child.classList.contains(platform) ? "none" : "block";
}