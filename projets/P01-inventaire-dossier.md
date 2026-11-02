---
id: P01
titre: Inventaire d'un dossier contractuel
type: outil public
statut: vérification (0.1.0, mode local)
priorité: à définir
source: zenzen-sol/legal-prompts, skill matter-intake (v0.4.0)
licence_source: MIT
dépend_de: [P11, P09]
mise_a_jour: 2026-10-31
---

# Inventaire d'un dossier contractuel

## 1. Origine

La skill matter-intake de Sol Irvine produit, à partir des documents d'un dossier, un instantané en .docx qui sert de registre des éléments probants : contrats, avenants, documents de négociation et de signature, en distinguant les documents contractuels de la correspondance, des modèles et des précédents. Le registre doit pouvoir être relu par l'avocat et repris par un agent lors d'une session ultérieure. Consulté le 2026-10-31 (en-tête et premières sections).

## 2. Problème ou opportunité

Reprendre un dossier contractuel (nouveau client, collaborateur absent, négociation qui reprend après des mois) demande de reconstituer quels documents existent, lesquels sont signés, quelle version fait foi. Ce travail est répétitif et souvent refait à chaque reprise.

## 3. Solution envisagée

L'avocat désigne un dossier local. L'outil classe les pièces, identifie pour chaque contrat sa version, son statut (projet, signé, modifié, résilié), ses parties et ses dates, et produit un registre en .docx et un résumé lisible par un agent.

Hors périmètre : analyse juridique des clauses, avis sur la validité, traitement de dossiers contentieux (une variante pourrait suivre).

## 4. Adaptation à jerlash.labs

Exécution locale ; seuls les extraits nécessaires partent vers le fournisseur choisi. Sortie en français. Vocabulaire belge (avenant, conditions particulières, mise en demeure). Option de pseudonymisation préalable via P09.

## 5. Approche technique pressentie

Script local (Python ou Node) : conversion des pièces en texte (P11), extraction structurée par le modèle, génération .docx. Reprendre les règles du standard `factory/standards/prompts-juridiques.md`.

## 6. Contraintes et risques

Déontologie : données de dossier envoyées au fournisseur ; l'avocat doit avoir vérifié son contrat avec celui-ci.
Réglementation : RGPD (données personnelles dans les pièces).
Technique : pièces scannées sans couche texte, courriels .msg/.eml.
Licence : MIT ; conserver la mention de copyright si du texte de la skill est repris. Une réécriture en français reste une adaptation : citer la source.

## 7. Critères d'acceptation

- [ ] Sur le jeu de test fictif F-DOSSIER-01, chaque document est classé et le statut des contrats est exact.
- [ ] Aucun original n'est modifié.
- [ ] Le registre .docx s'ouvre dans Word sans erreur.
- [ ] Le coût d'une exécution sur le jeu de test est mesuré et indiqué sur la fiche.

## 8. Appétit

Temps : [À COMPLÉTER]. Délai : [À COMPLÉTER].

## 9. Questions ouvertes

1. Quels formats de pièces faut-il couvrir dès la première version ?
2. Lien avec le logiciel de gestion du cabinet : aucun au départ, à confirmer.

## 10. Prochaine étape

0.1.0 livré le 2026-10-31 en mode local (outils/inventaire-dossier), mesuré sur F-DOSSIER-01 (dossier de développement et dossier de contrôle). Mode avec IA : ADR-015, proposée, à trancher par Florian.
