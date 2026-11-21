"""Dossier surveillé par scrutation périodique (bibliothèque standard seule).

Un fichier n'est pris en compte qu'une fois sa taille et sa date de modification
stables entre deux passages : on attend ainsi la fin de l'écriture. Une disparition
n'est confirmée qu'au passage suivant, ce qui permet de reconnaître un renommage
(même empreinte sous un autre nom).

Événements produits : creation, modification (même nom, contenu différent :
nouvelle version), renommage, suppression, illisible. Un fichier illisible est
signalé, jamais ignoré en silence.

L'identifiant d'un événement est dérivé de son contenu (type, chemin, empreinte,
version) et non de l'heure : rejouer le même événement donne le même identifiant.
"""

import hashlib
import json
import os

from .outils_fichiers import ecrire_json, empreinte_fichier, horodatage, lire_json


def identifiant_evenement(evenement: dict) -> str:
    cle = {k: evenement.get(k) for k in ("type", "chemin", "ancien_chemin", "sha256", "version", "signature")}
    return hashlib.sha256(json.dumps(cle, sort_keys=True).encode("utf-8")).hexdigest()[:32]


def _evenement(type_, chemin, **champs) -> dict:
    ev = {"type": type_, "chemin": chemin, "horodatage": horodatage()}
    ev.update({k: v for k, v in champs.items() if v is not None})
    ev["id"] = identifiant_evenement(ev)
    return ev


class Surveillant:
    """Observe un dossier et renvoie, à chaque passage, la liste des événements."""

    def __init__(self, racine: str, fichier_etat: str | None = None, lire_empreinte=empreinte_fichier):
        self.racine = os.path.abspath(racine)
        self.fichier_etat = fichier_etat
        self.lire_empreinte = lire_empreinte
        etat = lire_json(fichier_etat, {}) if fichier_etat else {}
        # fichiers stables déjà annoncés : chemin -> {taille, mtime_ns, sha256, version}
        self.connus: dict = etat.get("connus", {})
        # dernier numéro de version attribué à chaque nom
        self.versions: dict = etat.get("versions", {})
        # vus mais pas encore stables : chemin -> [taille, mtime_ns]
        self.en_attente: dict = {}
        # disparus non encore confirmés : chemin -> infos du fichier connu
        self.disparus: dict = {}
        # illisibles déjà signalés : chemin -> [taille, mtime_ns]
        self.signales: dict = {}

    def _lister(self) -> tuple[dict, list]:
        presents, illisibles = {}, []
        for dossier, sous_dossiers, fichiers in os.walk(self.racine):
            sous_dossiers.sort()
            for nom in sorted(fichiers):
                absolu = os.path.join(dossier, nom)
                relatif = os.path.relpath(absolu, self.racine).replace(os.sep, "/")
                try:
                    st = os.stat(absolu)
                except OSError as e:
                    illisibles.append((relatif, type(e).__name__, None))
                    continue
                presents[relatif] = [st.st_size, st.st_mtime_ns]
        return presents, illisibles

    def _illisible(self, chemin, erreur, meta) -> dict | None:
        if self.signales.get(chemin) == meta:
            return None  # déjà signalé, rien n'a changé depuis
        self.signales[chemin] = meta
        signature = "-".join(str(x) for x in meta) if meta else "stat"
        return _evenement("illisible", chemin, erreur=erreur,
                          taille=meta[0] if meta else None, signature=signature)

    def scruter(self) -> list[dict]:
        """Un passage de surveillance. Renvoie les événements, dans un ordre stable."""
        evenements = []
        presents, erreurs_stat = self._lister()
        for chemin, erreur, meta in erreurs_stat:
            ev = self._illisible(chemin, erreur, meta)
            if ev:
                evenements.append(ev)

        # 1. disparitions : confirmées au passage suivant (voir 4)
        confirmer = [c for c in self.disparus]
        for chemin in list(self.connus):
            if chemin not in presents:
                self.disparus[chemin] = self.connus.pop(chemin)
        for chemin in list(self.en_attente):
            if chemin not in presents:
                del self.en_attente[chemin]
        for chemin in list(self.signales):
            if chemin not in presents:
                del self.signales[chemin]

        # 2. fichiers stables
        stables = []
        for chemin, meta in presents.items():
            connu = self.connus.get(chemin)
            if connu and [connu["taille"], connu["mtime_ns"]] == meta:
                continue
            if self.en_attente.get(chemin) != meta and chemin not in self.signales:
                self.en_attente[chemin] = meta
                continue
            self.en_attente.pop(chemin, None)
            try:
                sha = self.lire_empreinte(os.path.join(self.racine, chemin.replace("/", os.sep)))
            except OSError as e:
                ev = self._illisible(chemin, type(e).__name__, meta)
                if ev:
                    evenements.append(ev)
                continue
            self.signales.pop(chemin, None)
            stables.append((chemin, meta, sha))

        # 3. classement des fichiers stables
        for chemin, meta, sha in stables:
            infos = {"taille": meta[0], "mtime_ns": meta[1], "sha256": sha}
            connu = self.connus.get(chemin) or self.disparus.pop(chemin, None)
            if connu and connu["sha256"] == sha:
                self.connus[chemin] = dict(connu, **infos)  # simple changement de date
                continue
            if connu:
                type_, ancien = "modification", None
            else:
                ancien = next((c for c, d in sorted(self.disparus.items()) if d["sha256"] == sha), None)
                type_ = "renommage" if ancien else "creation"
                if ancien:
                    del self.disparus[ancien]
            version = self.versions.get(chemin, 0) + 1
            self.versions[chemin] = version
            self.connus[chemin] = dict(infos, version=version)
            evenements.append(_evenement(type_, chemin, ancien_chemin=ancien, sha256=sha,
                                         taille=meta[0], version=version))

        # 4. suppressions confirmées (disparues depuis au moins un passage)
        for chemin in confirmer:
            infos = self.disparus.pop(chemin, None)
            if infos:
                evenements.append(_evenement("suppression", chemin, sha256=infos["sha256"],
                                             version=infos.get("version")))

        self._sauver()
        return evenements

    def _sauver(self) -> None:
        if self.fichier_etat:
            ecrire_json(self.fichier_etat, {"connus": self.connus, "versions": self.versions})
