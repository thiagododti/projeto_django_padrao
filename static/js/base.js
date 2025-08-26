document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.getElementById('hamburger')
    const sidebar = document.getElementById('sidebar')
    const menuSidebar = document.getElementById('menu_sidebar')

    hamburger.addEventListener('click', () => {
        sidebar.classList.toggle('-translate-x-full')
        sidebar.classList.toggle('w-64')
        sidebar.classList.toggle('p-4')


        menuSidebar.classList.toggle('hidden')



    })
})