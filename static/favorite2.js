const starContainers2 = document.querySelectorAll(".star-container");

for (let container of starContainers2){
    container.addEventListener("click", async function(e){
        console.log("HIIII", starContainers2)
        console.log(e.currentTarget.parentNode.id)
        if (e.currentTarget.firstElementChild.id=="full-star") e.currentTarget.parentNode.remove()

        
        const res = await axios.post(`/books/${e.currentTarget.parentNode.id}/favorite`)
    })
}