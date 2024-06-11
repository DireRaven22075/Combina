//소스코드 작성자 : 2023041004-한윤수
//지정한 destination으로 보내는 함수
function goto(dest) {
    //혹시 모르니 화면의 스크롤을 <0, 0> (맨 처음)으로 고정
    window.scrollTo(0, 0);
    //화면의 경로를 destination으로 이동
    window.location.href = dest;
    //함수 종료
    return;
}