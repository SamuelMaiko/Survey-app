

document.addEventListener("DOMContentLoad", ()=>{

    const showLoading=()=>{
        document.querySelector('.loadin'),style.display="block"
    }
    const hideLoading=()=>{
        document.querySelector('.loadin'),style.display="none"
    }

    document.ajaxStart=showLoading;
    document.ajaxStop=hideLoading;
    
})

// document.querySelector('.gridy__side').style.display="none"
menuBtn=document.querySelector('.gridy__menu')
sidePop=document.querySelector('.gridy__side')

sidePop.addEventListener('click', (e)=>{
    e.stopPropagation();
})

menuBtn.addEventListener('click', (e)=>{
    e.stopPropagation();
    sidePop.classList.toggle('hide');
})

cancelBtn=document.querySelector('.gridy__cancel')
cancelBtn.addEventListener('click',()=>{
    sidePop.classList.add('hide')
})

const containerDiv=document.querySelector('.container__div')
containerDiv.addEventListener('click', ()=>{
    sidePop.classList.add('hide')
})

const notifCancelBtn=document.querySelector('.notif__cancel')
// notifCancelBtn.style.display="none"
notifCancelBtn.addEventListener('click', ()=>{
    document.querySelector('.notif_div').style.display="none"
})
// const radioBtns=document.querySelector('.radio__buttons')
// radioBtns.style.display="none"
// if (radioBtns.checked ==true){
//     document.querySelector('.submitBtn').style.display="block"
// }
// else{
//     document.querySelector('.submitBtn').style.display="none"

// }


const intervalId=setInterval(()=>{
    document.querySelector('.notif_div').style.display="none"
}, 5000)