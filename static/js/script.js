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

