// document.addEventListener("DOMContentLoaded",()=>{

// })

const change_title = document.querySelector(".header-search h1");
const change_bg = document.querySelector("body");


function change_enter() {
  change_title.innerText = "끼아아아아아악"; 
  change_title.style.color = "red";
  change_bg.style.backgroundColor = "lightpink";
};

function change_leave() {
  change_title.innerText = "전체게시판";
  change_title.style.color = "black";
  change_bg.style.backgroundColor = "white";
};

change_title.addEventListener("mouseenter", change_enter);
change_title.addEventListener("mouseleave", change_leave);


// -- 두번째 기능 --
function aaaaaaaaa() {
  pass
};

change_title.addEventListener("mouseenter", change_enter);


