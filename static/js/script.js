// Scroll to the Top of the page refresh
if (history.scrollRestoration) {
    history.scrollRestoration = 'manual';
} else {
    window.onbeforeunload = function () {
        window.scrollTo(0, 0);
    }
}


// document.body.addEventListener('htmx:configRequest', (event) => {
//     event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
// })