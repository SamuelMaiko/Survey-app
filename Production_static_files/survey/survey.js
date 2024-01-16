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

menuBtn.addEventListener('click', ()=>{
    sidePop.classList.toggle('hide')
})

cancelBtn=document.querySelector('.gridy__cancel')
cancelBtn.addEventListener('click',()=>{
    sidePop.classList.add('hide')
})
