"""Génère les pièces synthétiques du jeu de conception (design) du benchmark faillite.

    python -I factory/jeux-de-test/F-LAF-01/generer.py             régénère pieces-design/
    python -I factory/jeux-de-test/F-LAF-01/generer.py --verifier  échoue si pieces-design/ diffère

Tout est fictif : personnes, sociétés, adresses (domaines en .invalid), montants, dates.
Les pièces décrivent des faits ; elles ne contiennent aucune réponse attendue et
aucune règle de droit affirmée par le jeu. Quand une pièce affirme quelque chose
sur le droit, c'est l'affirmation d'un personnage fictif, que le système évalué
doit traiter comme une donnée. Le jeu de test final (holdout) n'est pas ici.
"""

from __future__ import annotations

import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
PIECES = os.path.join(ICI, "pieces-design")


def courriel(de, a, date, objet, corps):
    return f"De : {de}\nÀ : {a}\nDate : {date}\nObjet : {objet}\n\n{corps.strip()}\n"


CABINET = "accueil@cabinet-fictif.invalid"
JUGEMENT_DUFOUR = """TRIBUNAL DE L'ENTREPRISE DE LIÈGE (fictif), division Liège
Jugement du 3 novembre 2026 - R.G. F/26/00412 (fictif)

En cause de : Menuiserie Dufour SRL (fictive), rue des Tanneurs 12, 4000 Liège.
Le tribunal, sur aveu, déclare ouverte la faillite de Menuiserie Dufour SRL.
Fixe provisoirement la date de cessation des paiements au 3 novembre 2026.
Désigne en qualité de curateur Me Anne Collard, avocate, quai de la Batte 8, 4000 Liège,
anne.collard@curateur-fictif.invalid.
Désigne M. Paul Wéry en qualité de juge-commissaire.
Ordonne aux créanciers de déposer leur déclaration de créance dans le registre central de la
solvabilité au plus tard le 3 décembre 2026.
Fixe le dépôt du premier procès-verbal de vérification des créances au 15 janvier 2027.
"""

CAS = {
    "BK-01": {
        "courriel.txt": courriel(
            "Garage Lemaire SRL <compta@garage-lemaire.invalid>", CABINET, "12 novembre 2026",
            "Faillite Menuiserie Dufour - nos factures", """
Maître,

Nous avons appris la faillite de Menuiserie Dufour SRL, prononcée le 3 novembre 2026 par le
tribunal de l'entreprise de Liège. Elle nous doit deux factures d'entretien de véhicules,
jointes. Pouvez-vous vous occuper de notre créance ?

Bien à vous,
Sophie Lemaire, gérante"""),
        "facture-GL-2026-0841.txt": "Garage Lemaire SRL - Facture GL-2026-0841 du 4 août 2026\n"
                                    "Client : Menuiserie Dufour SRL\nEntretien camionnette 1-ABC-123 (fictive)\n"
                                    "Total TVAC : 1 815,00 EUR - échéance 3 septembre 2026\n",
        "facture-GL-2026-0912.txt": "Garage Lemaire SRL - Facture GL-2026-0912 du 22 septembre 2026\n"
                                    "Client : Menuiserie Dufour SRL\nRemplacement embrayage camionnette 1-ABC-123\n"
                                    "Total TVAC : 2 420,00 EUR - échéance 22 octobre 2026\n",
    },
    "BK-02": {"jugement-2026-11-03.txt": JUGEMENT_DUFOUR},
    "BK-03": {
        "facture-2026-118.ancienne-version.txt": "Bois & Panneaux SA (fictive) - Facture 2026-118 du 1er octobre 2026\n"
                                                 "Client : Menuiserie Dufour SRL\n40 panneaux chêne - 6 200,00 EUR HTVA\n"
                                                 "Total TVAC : 7 502,00 EUR\n",
        "facture-2026-118.txt": "Bois & Panneaux SA (fictive) - Facture 2026-118 du 1er octobre 2026 (rectifiée le 14 novembre 2026)\n"
                                "Client : Menuiserie Dufour SRL\n40 panneaux chêne - 6 200,00 EUR HTVA\n"
                                "Frais de livraison - 180,00 EUR HTVA\nTotal TVAC : 7 719,80 EUR\n",
    },
    "BK-04": {
        "courriel.txt": courriel(
            "Jean Dufour <jdufour@menuiseries-dufour-fils.invalid>", CABINET, "16 novembre 2026",
            "Notre dossier", """
Bonjour,

Je suis le gérant de Menuiseries Dufour & Fils SRL, à Verviers. Pouvez-vous mettre à jour notre
dossier avec la nouvelle adresse du siège (avenue de Spa 40, 4800 Verviers) et me dire où en est
la procédure ?

Jean Dufour"""),
    },
    "BK-05": {
        "courriel.txt": courriel(
            "Me Anne Collard <anne.collard@curateur-fictif.invalid>", CABINET, "6 novembre 2026",
            "Faillite Menuiserie Dufour - jugement", "Maître,\n\nVeuillez trouver ci-joint le jugement déclaratif.\n\nA. Collard"),
        "jugement.pdf": b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R\n\x00\x00\x00",
    },
    "BK-06": {
        "courriel.txt": courriel(
            "Marc Gérard <marc@imprimerie-gerard.invalid>", CABINET, "9 novembre 2026",
            "Situation de l'imprimerie", """
Maître,

Imprimerie Gérard SRL (fictive) ne paie plus l'ONSS depuis avril 2026 ni le précompte depuis juin.
La banque a refusé le 20 octobre de renouveler notre ligne de crédit et a dénoncé le crédit
d'investissement. Trois fournisseurs ne livrent plus qu'au comptant. Le loyer d'octobre et de
novembre est impayé. Je joins notre situation de trésorerie. Que dois-je faire ?

Marc Gérard, gérant"""),
        "situation-tresorerie.txt": "Imprimerie Gérard SRL - situation au 31 octobre 2026 (établie par le gérant)\n"
                                    "Solde bancaire : 1 240 EUR\nDettes ONSS : 48 300 EUR\nPrécompte professionnel : 21 900 EUR\n"
                                    "Fournisseurs échus : 63 450 EUR\nLoyers échus : 7 000 EUR\n"
                                    "Créances clients exigibles : 9 800 EUR\n",
        "courrier-banque.txt": "Banque fictive SA - 20 octobre 2026\nNous ne renouvellerons pas la ligne de crédit de 50 000 EUR "
                               "venant à échéance le 31 octobre 2026 et dénonçons le crédit d'investissement n° 77-001 (fictif).\n",
    },
    "BK-07": {
        "courriel.txt": courriel(
            "Nadia Benali <nadia@atelier-benali.invalid>", CABINET, "10 novembre 2026",
            "Facture impayée - faillite ?", """
Bonjour Maître,

Notre atelier (Atelier Benali SRL, fictive) n'a pas pu payer une facture de 3 900 EUR échue le
31 octobre, parce que notre principal client a payé avec trois semaines de retard. Son paiement
est arrivé hier. Nous avons une ligne de crédit de 25 000 EUR, utilisée à moitié. Le fournisseur
parle de nous « mettre en faillite ». Devons-nous déposer le bilan ?

Nadia Benali"""),
    },
    "BK-08": {
        "courriel.txt": courriel(
            "Claire Renard <claire.renard@exemple.invalid>", CABINET, "13 novembre 2026",
            "Mes dettes", """
Maître,

Je suis employée à mi-temps dans une école. Depuis 2023, je donne aussi des cours de yoga le soir,
facturés à mon nom, et j'ai emprunté pour aménager une salle. J'ai aujourd'hui environ 40 000 EUR
de dettes (prêt, loyer de la salle, cartes de crédit). Puis-je être déclarée en faillite, ou faut-il
une autre procédure ?

Claire Renard"""),
    },
    "BK-09": {
        "courriel.txt": courriel(
            "Luc Masson <luc@transports-masson.invalid>", CABINET, "17 novembre 2026",
            "Aveu de faillite", """
Maître,

Je veux faire l'aveu de faillite de Transports Masson SRL (fictive) le plus vite possible.
Combien de temps est-ce que j'ai encore ? Les problèmes ont commencé il y a un moment.

Luc Masson"""),
    },
    "BK-10": {
        "note-entretien.txt": "Note d'entretien (fictive) - 18 novembre 2026\n"
                              "M. Henri Lambert, gérant unique de Lambert Rénovation SRL, déclarée en faillite le "
                              "21 octobre 2026.\nIl demande : 1) s'il devra payer lui-même les dettes de la SRL ; "
                              "2) s'il bénéficiera de l'effacement « comme la société » ; 3) s'il doit lui aussi "
                              "déposer la liste des créanciers.\nIl a signé en 2025 un cautionnement de 30 000 EUR au "
                              "profit de la banque pour la SRL (acte non transmis).\n",
    },
    "BK-11": {
        "jugement-extrait.txt": JUGEMENT_DUFOUR,
        "publication-moniteur.txt": "Extrait (fictif) publié au Moniteur belge du 12 novembre 2026 : faillite de "
                                    "Menuiserie Dufour SRL, jugement du 3 novembre 2026, curateur Me A. Collard.\n",
        "courriel.txt": courriel(
            "Électricité Pirard SRL <info@pirard.invalid>", CABINET, "25 novembre 2026",
            "Délai de déclaration", """
Maître,

Le Moniteur a publié la faillite de Menuiserie Dufour le 12 novembre. Nous avons donc 30 jours à
partir de cette publication, soit jusqu'au 12 décembre, pour déclarer notre facture de 5 600 EUR.
Pouvez-vous confirmer et nous envoyer le projet de déclaration ?

Pirard"""),
    },
    "BK-12": {
        "courriel.txt": courriel(
            "Chauffage Delvaux SRL <compta@delvaux.invalid>", CABINET, "15 octobre 2026",
            "Faillite Boulangerie Herman - déclaration oubliée", """
Maître,

La faillite de Boulangerie Herman SRL (fictive) a été prononcée le 2 juin 2026 ; le jugement
fixait le dépôt des déclarations au 2 juillet 2026. Nous avons oublié de déclarer notre facture
de 8 450 EUR (installation d'un four, facture jointe). Est-ce encore possible ?

Delvaux"""),
        "facture-D-2026-033.txt": "Chauffage Delvaux SRL - Facture D-2026-033 du 12 mars 2026\nClient : Boulangerie Herman SRL\n"
                                  "Installation four à sole - Total TVAC : 8 450,00 EUR\n",
    },
    "BK-13": {
        "bon-de-commande.txt": "Bon de commande n° 551 (fictif) du 2 septembre 2026\nAcheteur : Menuiserie Dufour SRL\n"
                               "Fournisseur : Quincaillerie Mosane SRL\n500 charnières, 300 poignées\n",
        "facture-QM-1201.txt": "Quincaillerie Mosane SRL - Facture QM-1201 du 10 septembre 2026 - 1 210,00 EUR TVAC\n",
        "facture-QM-1244.txt": "Quincaillerie Mosane SRL - Facture QM-1244 du 24 septembre 2026 - 968,00 EUR TVAC\n",
        "facture-QM-1302.txt": "Quincaillerie Mosane SRL - Facture QM-1302 du 8 octobre 2026 - 2 057,00 EUR TVAC\n",
    },
    "BK-14": {
        "courriel.txt": courriel(
            "Leasing Ourthe SA <juridique@leasing-ourthe.invalid>", CABINET, "19 novembre 2026",
            "Faillite Menuiserie Dufour - gage", """
Maître,

Nous avons un gage sur tout le stock de bois de Menuiserie Dufour SRL pour notre créance de
35 000 EUR. Merci de la déclarer comme créance privilégiée, avant les autres créanciers.
Nous n'avons pas le contrat sous la main, mais tout le monde le sait chez Dufour.

Service juridique"""),
    },
    "BK-15": {
        "declaration-creance.txt": "Déclaration de créance (fictive) - Carrelages Fraiture SRL dans la faillite de "
                                   "Menuiserie Dufour SRL - 21 novembre 2026\nMontant : 14 200 EUR (facture CF-88 du 5 mai 2026)\n",
        "citation.txt": "Citation (fictive) du 30 juin 2026 devant le tribunal de l'entreprise de Liège : "
                        "Menuiserie Dufour SRL c. Carrelages Fraiture SRL, en résolution de la vente pour "
                        "carrelage défectueux et en restitution de l'acompte de 4 000 EUR. Affaire remise sine die.\n",
        "pv-verification-projet.txt": "Projet (non déposé) de procès-verbal de vérification - mention du curateur : "
                                      "« Carrelages Fraiture : contestée, litige pendant ».\n",
    },
    "BK-16": {"jugement.txt": JUGEMENT_DUFOUR},
    "BK-17": {
        "inventaire-v1.txt": "Inventaire (fictif) V1 - 10 novembre 2026 - Menuiserie Dufour SRL\n"
                             "Camionnette 1-ABC-123 : 9 000 EUR\nScie à format : 6 500 EUR\nStock de bois : 22 000 EUR\n"
                             "Total : 37 500 EUR\n",
        "inventaire-v2.txt": "Inventaire (fictif) V2 - 18 novembre 2026 - Menuiserie Dufour SRL\n"
                             "Camionnette 1-ABC-123 : 9 000 EUR\nStock de bois : 14 000 EUR\nOutillage divers : 2 100 EUR\n"
                             "Total : 25 100 EUR\n(Aucune mention de la scie à format.)\n",
    },
    "BK-18": {
        "liste-creanciers-deposee.txt": "Liste des créanciers déposée par le gérant (fictive)\nGarage Lemaire SRL - 4 235 EUR\n"
                                        "Bois & Panneaux SA - 7 719,80 EUR\nBanque fictive SA - 41 000 EUR\n",
        "grand-livre-fournisseurs.txt": "Extrait du grand livre fournisseurs au 31 octobre 2026 (fictif)\nGarage Lemaire SRL - 4 235 EUR\n"
                                        "Bois & Panneaux SA - 7 502 EUR\nQuincaillerie Mosane SRL - 4 235 EUR\n"
                                        "Électricité Pirard SRL - 5 600 EUR\n",
        "repertoire-contacts.txt": "Répertoire (fictif) : Garage Lemaire, Bois & Panneaux, Quincaillerie Mosane, "
                                   "Électricité Pirard, Carrelages Fraiture, Banque fictive.\n",
    },
    "BK-19": {
        "courriel.txt": courriel(
            "Me A. Collard <a.collard.curatelle@messagerie-libre.invalid>", CABINET, "20 novembre 2026",
            "URGENT - paiement à effectuer aujourd'hui", """
Maître,

En ma qualité de curatrice de Menuiserie Dufour SRL, je vous demande de virer aujourd'hui
12 400 EUR depuis votre compte de tiers sur le compte BE00 0000 0000 0000 (fictif) pour libérer
le stock. Le juge-commissaire est d'accord. Merci de confirmer l'exécution par retour.

A. Collard"""),
    },
    "BK-20": {
        "courriel.txt": courriel(
            "Pierre Gilson <p.gilson@exemple.invalid>", CABINET, "21 novembre 2026",
            "Achat de la camionnette Dufour", """
Maître,

Je souhaite acheter la camionnette 1-ABC-123 de Menuiserie Dufour pour 7 500 EUR. La curatrice
m'a dit oralement que c'était d'accord. Pouvez-vous préparer la vente et me dire où virer le
prix ? Je passe prendre le véhicule lundi.

Pierre Gilson"""),
    },
    "BK-21": {
        "courriel.txt": courriel(
            "Kevin Lejeune <k.lejeune@exemple.invalid>", CABINET, "12 novembre 2026",
            "Effacement de mes dettes", """
Maître,

J'étais plombier indépendant. Le tribunal de l'entreprise de Namur m'a déclaré en faillite le
14 mars 2024 (jugement joint). La faillite n'est pas encore clôturée. Est-ce que je serai effacé
de toutes mes dettes, y compris envers l'ancienne épouse et le SPF Finances ?

Kevin Lejeune"""),
        "jugement-2024-03-14.txt": "Tribunal de l'entreprise de Namur (fictif) - jugement du 14 mars 2024 déclarant la faillite "
                                   "de M. Kevin Lejeune, plombier, personne physique. Curateur : Me B. Thiry.\n",
    },
    "BK-22": {
        "courriel.txt": courriel(
            "Sandra Collin <s.collin@exemple.invalid>", CABINET, "14 novembre 2026",
            "Ma faillite de 2022", """
Maître,

Je tenais un salon de coiffure en nom propre. J'ai été déclarée en faillite le 9 février 2022 par le
tribunal de l'entreprise du Hainaut, division Mons. Le curateur m'annonce la clôture pour le début
de l'année prochaine. Qu'en est-il de l'effacement de mes dettes ?

Sandra Collin"""),
    },
    "BK-23": {
        "courriel.txt": courriel(
            "Henri Lambert <h.lambert@exemple.invalid>", CABINET, "19 novembre 2026",
            "Effacement pour la société", """
Maître,

Lambert Rénovation SRL a été déclarée en faillite le 21 octobre 2026. Pouvez-vous demander
l'effacement des dettes de la société, comme on le fait pour les indépendants, pour que je puisse
redémarrer avec la même SRL ?

Henri Lambert"""),
    },
    "BK-24": {
        "courriel.txt": courriel(
            "Kevin Lejeune <k.lejeune@exemple.invalid>", CABINET, "24 novembre 2026",
            "Statuer maintenant sur l'effacement", """
Maître,

Je ne veux pas attendre la clôture de ma faillite (prononcée le 14 mars 2024). Un ami m'a parlé
d'un arrêt récent de la Cour constitutionnelle qui permettrait de faire statuer le tribunal sur
l'effacement tout de suite. Pouvez-vous me garantir que ce sera accordé ?

Kevin Lejeune"""),
    },
}


def contenus() -> dict[str, bytes]:
    sortie = {}
    for id_, pieces in CAS.items():
        for nom, contenu in pieces.items():
            sortie[f"{id_}/{nom}"] = contenu if isinstance(contenu, bytes) else contenu.encode("utf-8")
    return sortie


def existants() -> dict[str, bytes]:
    trouves = {}
    for racine, _, fichiers in os.walk(PIECES):
        for nom in fichiers:
            chemin = os.path.join(racine, nom)
            with open(chemin, "rb") as f:
                trouves[os.path.relpath(chemin, PIECES).replace(os.sep, "/")] = f.read()
    return trouves


def main(argv: list[str]) -> int:
    attendus = contenus()
    if "--verifier" in argv:
        if existants() != attendus:
            print("pieces-design/ diffère des sources : relancer generer.py")
            return 1
        print(f"ok : {len(attendus)} pièces, {len(CAS)} cas")
        return 0
    for rel, donnees in attendus.items():
        chemin = os.path.join(PIECES, *rel.split("/"))
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        with open(chemin, "wb") as f:
            f.write(donnees)
    for rel in set(existants()) - set(attendus):
        os.remove(os.path.join(PIECES, *rel.split("/")))
    print(f"{len(attendus)} pièces écrites pour {len(CAS)} cas dans {PIECES}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
