//import { nextPlatform, prevPlatform } from './interacts/navigation.js';
import { goto } from './interacts/menubar.js';
document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("keydown", function (e) {
        console.log(e.key);
        switch (e.key) {
            case "ArrowLeft": case "a":
                break;
            case "ArrowRight": case "d":
                //nextPlatform();
                break;
            case "ArrowUp": case "w":
                nextService();
                break;
            case "ArrowDown": case "s":
                prevService();
                break;
        }
    });
});
function nextService() {
    switch (document.title.split(" : ")[1]) {
        case "Home": goto("/explore"); return;
        case "Explore": goto("/contacts"); return;
        case "Contacts": goto("/watch"); return;
        case "Watch": goto("/create"); return;
        case "Create": goto("/home"); return;
    }
}
function prevService() {
    switch (document.title.split(" : ")[1]) {
        case "Home": goto("/create"); return;
        case "Explore": goto("/home"); return;
        case "Contacts": goto("/explore"); return;
        case "Watch": goto("/contacts"); return;
        case "Create": goto("/watch"); return;
    }
}