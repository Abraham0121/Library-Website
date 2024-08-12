// implement book hold functionality

const bookmarkContainers = document.querySelectorAll(".bookmark-container");

for (let container of bookmarkContainers){
    container.addEventListener("click", async function(e){
        console.log("HIIII")
        if (e.currentTarget.firstElementChild.id=="empty-bookmark"){
            console.log("NUmBER1")
            container.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="35px" height="40px"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M0 48V487.7C0 501.1 10.9 512 24.3 512c5 0 9.9-1.5 14-4.4L192 400 345.7 507.6c4.1 2.9 9 4.4 14 4.4c13.4 0 24.3-10.9 24.3-24.3V48c0-26.5-21.5-48-48-48H48C21.5 0 0 21.5 0 48z"/></svg>';
            container.firstChild.id = 'full-bookmark';
        } else if (e.currentTarget.firstElementChild.id=="full-bookmark"){
            container.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="35px" height="40px"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M0 48C0 21.5 21.5 0 48 0l0 48 0 393.4 130.1-92.9c8.3-6 19.6-6 27.9 0L336 441.4 336 48 48 48 48 0 336 0c26.5 0 48 21.5 48 48l0 440c0 9-5 17.2-13 21.3s-17.6 3.4-24.9-1.8L192 397.5 37.9 507.5c-7.3 5.2-16.9 5.9-24.9 1.8S0 497 0 488L0 48z"/></svg>';
            container.firstChild.id = 'empty-bookmark';
        }
        
        const res = await axios.post(`/books/${e.currentTarget.parentNode.id}/hold`)
    })
}