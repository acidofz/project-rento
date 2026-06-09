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

  window.__uyClickInitMap = function (markers, focusId) {
    var el = document.getElementById("uy-click-map");
    if (!el || typeof L === "undefined") return;

    if (el.__uyClickMap) {
      el.__uyClickMap.remove();
      el.__uyClickMap = null;
    }
    el.innerHTML = "";

    var map = L.map(el).setView([41.31, 69.28], 11);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: "&copy; OpenStreetMap",
    }).addTo(map);
    el.__uyClickMap = map;

    var bounds = [];
    var focusMarker = null;
    var focusLatLng = null;

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
      var imgHtml = m.image_url
        ? '<img src="' + escapeHtml(m.image_url) + '" style="width:100%;max-height:100px;object-fit:cover;border-radius:4px;margin-bottom:4px;" /><br/>'
        : "";
      marker.bindPopup(
        imgHtml +
          "<b>" + escapeHtml(title) + "</b><br/>" +
          escapeHtml(price) +
          '<br/><a href="' + escapeHtml(url) + '">Открыть →</a>'
      );

      if (focusId && m.id === focusId) {
        focusMarker = marker;
        focusLatLng = [lat, lng];
      }
    }

    if (focusMarker && focusLatLng) {
      map.setView(focusLatLng, 16);
      focusMarker.openPopup();
    } else if (bounds.length > 0) {
      map.fitBounds(bounds, { padding: [48, 48], maxZoom: 15 });
    }
  };
})();
