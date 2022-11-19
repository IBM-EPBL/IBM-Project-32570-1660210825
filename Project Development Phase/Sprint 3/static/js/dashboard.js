const modala = document.querySelector(".modala");
const triggera = document.querySelector("#triggera");
const closeButtona = document.querySelector(".close-buttona");
function toggleModala() {
modala.classList.toggle("show-modala");
}
function windowOnClicka(event) {
if (event.target === modala)    toggleModala();
}
triggera.addEventListener("click", toggleModala);
closeButtona.addEventListener("click", toggleModala);
window.addEventListener("click", windowOnClicka);



const modalu = document.querySelector(".modalu");
const triggeru = document.querySelector("#triggeru");
const closeButtonu = document.querySelector(".close-buttonu");
function toggleModalu() {
modalu.classList.toggle("show-modalu");
}
function windowOnClicku(event) {
if (event.target === modalu)    toggleModalu();
}
triggeru.addEventListener("click", toggleModalu);
closeButtonu.addEventListener("click", toggleModalu);
window.addEventListener("click", windowOnClicku);



const modald = document.querySelector(".modald");
const triggerd = document.querySelector("#triggerd");
const closeButtond = document.querySelector(".close-buttond");
function toggleModald() {
modald.classList.toggle("show-modald");
}

function windowOnClickd(event) {
if (event.target === modald)    toggleModald();
}
triggerd.addEventListener("click", toggleModald);
closeButtond.addEventListener("click", toggleModald);
window.addEventListener("click", windowOnClickd);
