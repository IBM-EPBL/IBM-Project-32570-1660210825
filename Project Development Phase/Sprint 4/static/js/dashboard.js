window.watsonAssistantChatOptions = {
    integrationID: "9321840d-f95b-41ee-bc97-781f200296ed", // The ID of this integration.
    region: "eu-gb", // The region your integration is hosted in.
    serviceInstanceID: "48d8d8e4-5faa-42e5-a7ec-2e061f99851c", // The ID of your service instance.
    onLoad: function(instance) { instance.render(); }
  };
  setTimeout(function(){
    const t=document.createElement('script');
    t.src="https://web-chat.global.assistant.watson.appdomain.cloud/versions/" + (window.watsonAssistantChatOptions.clientVersion || 'latest') + "/WatsonAssistantChatEntry.js";
    document.head.appendChild(t);
  });

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