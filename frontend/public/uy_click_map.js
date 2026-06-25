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
    if (!el || typeof ymaps === "undefined") return;

    if (el.__uyClickYMap) {
      try { el.__uyClickYMap.destroy(); } catch (e) { /* ignore */ }
      el.__uyClickYMap = null;
    }
    el.innerHTML = "";

    ymaps.ready(function () {
      var map = new ymaps.Map(el, {
        center: [39.6547, 66.9758],
        zoom: 12,
        controls: ["zoomControl", "fullscreenControl"],
      });
      el.__uyClickYMap = map;

      var focusPlacemark = null;
      var focusCoords = null;

      for (var i = 0; i < markers.length; i++) {
        var m = markers[i];
        var lat = Number(m.lat);
        var lng = Number(m.lng);
        if (!isFinite(lat) || !isFinite(lng)) continue;

        var title = escapeHtml((m.title || "Объект") + "");
        var price = escapeHtml((m.price || "") + "");
        var url = escapeHtml((m.url || "") + "");
        var imgHtml = m.image_url
          ? '<img src="' + escapeHtml(m.image_url) + '" style="width:100%;max-height:100px;object-fit:cover;border-radius:4px;margin-bottom:6px;" />'
          : "";

        var pm = new ymaps.Placemark(
          [lat, lng],
          {
            balloonContent:
              imgHtml +
              "<b>" + title + "</b><br/>" +
              price +
              '<br/><a href="' + url + '" style="color:#0d9488;">Открыть →</a>',
            hintContent: title,
          },
          { preset: "islands#tealDotIcon" }
        );
        map.geoObjects.add(pm);

        if (focusId && m.id === focusId) {
          focusPlacemark = pm;
          focusCoords = [lat, lng];
        }
      }

      if (focusPlacemark && focusCoords) {
        map.setCenter(focusCoords, 16);
        focusPlacemark.balloon.open();
      } else if (markers.length > 0) {
        try {
          map.setBounds(map.geoObjects.getBounds(), {
            checkZoomRange: true,
            zoomMargin: 48,
          });
        } catch (e) { /* ignore if no bounds */ }
      }
    });
  };
})();
