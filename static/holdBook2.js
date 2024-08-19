const bookmarkContainers = document.querySelectorAll(".bookmark-container-onhold");

for (let container of bookmarkContainers){
    container.addEventListener("click", async function(e){
        console.log("HIIII")
        if (e.currentTarget.firstElementChild.id=="full-bookmark") e.currentTarget.parentNode.remove()

        
        const res = await axios.post(`/books/${e.currentTarget.parentNode.id}/hold`)
    })
}