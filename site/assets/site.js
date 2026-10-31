// Scroll reveal. Progressive enhancement only: every page is fully readable without this file.
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.documentElement.classList.add('js');
  var sel = 'main h1, main h2, main h3, main p, main figure, main li, main .stage, main dl';
  var els = [].filter.call(document.querySelectorAll(sel), function (el) {
    // .enter blocks animate once on page load (CSS), so they skip the scroll reveal
    return !el.parentElement.closest(sel) && !el.closest('.enter, .hero');
  });
  els.forEach(function (el) { el.classList.add('reveal'); });
  var io = new IntersectionObserver(function (entries) {
    var i = 0; // stagger restarts for each batch that enters the viewport
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      var el = e.target;
      setTimeout(function () { el.classList.add('in'); }, Math.min(i++, 6) * 70);
    });
  });
  requestAnimationFrame(function () { els.forEach(function (el) { io.observe(el); }); });
})();
