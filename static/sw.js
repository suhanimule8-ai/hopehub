self.addEventListener("install", function () {
    console.log("HopeHub App Installed");
});

self.addEventListener("fetch", function (event) {
    event.respondWith(fetch(event.request));
});