// ASN FARMS - small UI helpers
(function () {
  document.documentElement.classList.add("js");

  // sticky nav shadow
  var nav = document.getElementById("nav");
  function onScroll() { if (nav) nav.classList.toggle("scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // mobile menu
  var burger = document.getElementById("burger");
  var links = document.getElementById("links");
  if (burger && links) {
    burger.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // reveal on scroll
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e, i) {
        if (e.isIntersecting) {
          e.target.style.transitionDelay = Math.min(i * 70, 350) + "ms";
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  // count-up numbers on the home page
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (!target || target < 2) return;
    var start = null;
    function tick(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / 1200, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    }
    el.textContent = "0";
    requestAnimationFrame(tick);
  });

  // image preview on the seller form
  var fileInput = document.querySelector('input[type="file"]');
  var preview = document.getElementById("preview");
  var dropText = document.getElementById("drop-text");
  if (fileInput && preview) {
    fileInput.addEventListener("change", function () {
      var f = fileInput.files && fileInput.files[0];
      if (!f) return;
      preview.src = URL.createObjectURL(f);
      preview.hidden = false;
      if (dropText) dropText.textContent = "✔ " + f.name + " (tap to change)";
    });
  }

  // numeric-only mobile fields
  document.querySelectorAll('input[inputmode="numeric"]').forEach(function (inp) {
    inp.addEventListener("input", function () {
      inp.value = inp.value.replace(/[^\d+\s-]/g, "");
    });
  });
})();
