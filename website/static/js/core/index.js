let angledownButton = document.querySelectorAll(".faAngle")
let show = document.querySelectorAll(".show")
console.log(angledownButton);
let idCheck = document.querySelectorAll(".idCheck")

for(let i=0;i<idCheck.length;i++){
    idCheck[i].addEventListener("click",function(){
        if(angledownButton[i].classList.contains("fa-angle-down")){
            angledownButton[i].classList.remove("fa-angle-down")
            angledownButton[i].classList.add("fa-angle-up")
            show[i].classList.remove("d-none")
            }
            else{
                angledownButton[i].classList.remove("fa-angle-up")
                angledownButton[i].classList.add("fa-angle-down")
                show[i].classList.add("d-none")
            }
    })
}
function faAngleChange(id) {
    return;
   
}