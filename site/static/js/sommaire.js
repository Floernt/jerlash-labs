/* Sommaire actif (ADR-033). Aucun accès réseau, aucune dépendance.
   Marque dans le sommaire latéral (partiel _partials/sommaire.html) l'intertitre en cours de lecture :
   le dernier dont le haut a franchi le quart supérieur de la fenêtre. Le lien reçoit aria-current="location".
   Si le sommaire est plus long que sa colonne, la colonne défile pour garder le lien visible.
   Sans JavaScript, le sommaire reste un simple sommaire. */
(function () {
  "use strict";
  var nav = document.querySelector(".sommaire--lateral");
  if (!nav || !window.requestAnimationFrame) return;

  var paires = [];
  Array.prototype.forEach.call(nav.querySelectorAll('a[href^="#"]'), function (lien) {
    var id;
    try { id = decodeURIComponent(lien.getAttribute("href").slice(1)); } catch (e) { return; }
    var titre = document.getElementById(id);
    if (titre) paires.push({ lien: lien, titre: titre });
  });
  if (!paires.length) return;

  var colonne = nav.parentNode;
  var actif = null;
  var attente = false;

  function garderVisible(lien) {
    if (colonne.scrollHeight <= colonne.clientHeight) return;
    var c = colonne.getBoundingClientRect();
    var l = lien.getBoundingClientRect();
    var marge = 24;
    if (l.top < c.top + marge) colonne.scrollTop -= c.top + marge - l.top;
    else if (l.bottom > c.bottom - marge) colonne.scrollTop += l.bottom - (c.bottom - marge);
  }

  function mettreAJour() {
    attente = false;
    var seuil = window.innerHeight * 0.25;
    var courant = null;
    for (var i = 0; i < paires.length; i += 1) {
      if (paires[i].titre.getBoundingClientRect().top <= seuil) courant = paires[i];
      else break;
    }
    // En bas de page, les derniers intertitres ne franchissent jamais le seuil : le dernier devient actif.
    var racine = document.documentElement;
    if (window.innerHeight + window.pageYOffset >= racine.scrollHeight - 2) courant = paires[paires.length - 1];
    if (courant === actif) return;
    if (actif) actif.lien.removeAttribute("aria-current");
    actif = courant;
    if (!actif) return;
    actif.lien.setAttribute("aria-current", "location");
    garderVisible(actif.lien);
  }

  function demander() {
    if (attente) return;
    attente = true;
    window.requestAnimationFrame(mettreAJour);
  }

  window.addEventListener("scroll", demander, { passive: true });
  window.addEventListener("resize", demander);
  mettreAJour();
})();
