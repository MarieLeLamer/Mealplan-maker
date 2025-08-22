let btn = document.getElementById('generate')
let divMenu = document.getElementById('menu')
let divCourse = document.getElementById('listeCourse')

btn.addEventListener('click', async () => {
    let response = await fetch('/getMenu')
    let menu = await response.json()
    console.log(menu)
    let str = ''
    for (const i in menu){
        str+= `${i}: ${menu[i]} \n`
    }
    divMenu.innerText = str
})
