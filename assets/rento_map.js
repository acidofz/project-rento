/* global L */
(function () {
  "use strict";

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  window.__rentoInitMap = function (markers) {
    var el = document.getElementById("rento-map");
    if (!el || typeof L === "undefined") return;

    if (el.__rentoMap) {
      el.__rentoMap.remove();
      el.__rentoMap = null;
    }
    el.innerHTML = "";

    var map = L.map(el).setView([41.31, 69.28], 11);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap",
    }).addTo(map);
    el.__rentoMap = map;

    var bounds = [];
    for (var i = 0; i < markers.length; i++) {
      var m = markers[i];
      var lat = Number(m.lat);
      var lng = Number(m.lng);
      if (!isFinite(lat) || !isFinite(lng)) continue;
      bounds.push([lat, lng]);
      var marker = L.marker([lat, lng]).addTo(map);
      var title = (m.title || "Объявление") + "";
      var price = (m.price || "") + "";
      var url = (m.url || "") + "";
      marker.bindPopup(
        "<b>" +
          escapeHtml(title) +
          "</b><br/>" +
          escapeHtml(price) +
          '<br/><a href="' +
          escapeHtml(url) +
          '">Открыть</a>'
      );
    }
    if (bounds.length > 0) {
      map.fitBounds(bounds, { padding: [48, 48], maxZoom: 15 });
    }
  };
})();
