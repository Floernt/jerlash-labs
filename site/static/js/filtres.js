/* Filtrage des listes par étiquette (ADR-032). Aucun accès réseau, aucune dépendance.
   Balisage attendu (partiel _partials/filtres.html) :
     <div data-filtres="<clé>" data-cible="<id de la grille>" hidden> <button data-valeur="">…</button> … </div>
     <div id="<id>"> <… data-<clé>="valeur1 valeur2"> … </div>
   Sans JavaScript, la barre reste cachée et tout le contenu s'affiche.
   Le filtre choisi est reporté dans l'adresse (?<clé>=valeur) pour qu'elle soit partageable. */
(function () {
  "use strict";
  var barres = document.querySelectorAll("[data-filtres]");
  Array.prototype.forEach.call(barres, function (barre) {
    var cle = barre.getAttribute("data-filtres");
    var cible = document.getElementById(barre.getAttribute("data-cible"));
    if (!cle || !cible) return;
    var elements = cible.querySelectorAll("[data-" + cle + "]");
    var boutons = barre.querySelectorAll("button[data-valeur]");
    var compte = barre.querySelector("[data-filtres-compte]");

    function valeurs(el) {
      return (el.getAttribute("data-" + cle) || "").split(/\s+/);
    }

    function appliquer(valeur, majAdresse) {
      var visibles = 0;
      Array.prototype.forEach.call(boutons, function (b) {
        b.setAttribute("aria-pressed", String(b.getAttribute("data-valeur") === valeur));
      });
      Array.prototype.forEach.call(elements, function (el) {
        var masque = valeur !== "" && valeurs(el).indexOf(valeur) === -1;
        el.hidden = masque;
        if (!masque) visibles += 1;
      });
      if (compte) compte.textContent = String(visibles);
      if (majAdresse && window.history && window.URL) {
        var adresse = new URL(window.location.href);
        if (valeur) adresse.searchParams.set(cle, valeur);
        else adresse.searchParams.delete(cle);
        window.history.replaceState(null, "", adresse.toString());
      }
    }

    Array.prototype.forEach.call(boutons, function (b) {
      b.addEventListener("click", function () {
        appliquer(b.getAttribute("data-valeur"), true);
      });
    });

    var initiale = "";
    if (window.URL) initiale = new URL(window.location.href).searchParams.get(cle) || "";
    var connue = Array.prototype.some.call(boutons, function (b) {
      return b.getAttribute("data-valeur") === initiale;
    });
    appliquer(connue ? initiale : "", false);
    barre.hidden = false;
  });
})();
