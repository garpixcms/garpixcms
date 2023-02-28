window.addEventListener("DOMContentLoaded", () => {
  if ("isStaff" in document.body.dataset === true) {
    navigator.serviceWorker.getRegistrations().then(function (registrations) {
      for (let registration of registrations) {
        registration.unregister();
      }
    });
  }
});
