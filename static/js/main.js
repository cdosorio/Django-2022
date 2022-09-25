let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

if (searchForm){
    for(let i=0; pageLinks.length > i; i++){
        pageLinks[i].addEventListener('click', function (e) {
            e.preventDefault();
            let page = this.dataset.page
            // template literal with backticks
            searchForm.innerHTML +=  `<input value=${page} name="page" hidden/>`
            searchForm.submit()
        })
    }
}
