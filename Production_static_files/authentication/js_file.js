const messages=document.querySelectorAll('.success')

const timeoutId=setTimeout(()=>{
    messages.forEach((each)=>{
        each.style.display='none';
    })
},3000)