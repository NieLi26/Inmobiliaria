// Scroll to the Top of the page refresh
// if (history.scrollRestoration) {
//   history.scrollRestoration = "manual";
// } else {
//   window.onbeforeunload = function () {
//     window.scrollTo(0, 0);
//   };
// }

if (history.replaceState) {
    history.replaceState(null, null, location.href);
}

// csrftoken cookie 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');