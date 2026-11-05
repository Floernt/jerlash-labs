---
id: P06
titre: Simulateur de négociation contractuelle
type: outil public
statut: idée
priorité: basse (dépend de P04 et P10)
source: zenzen-sol/wargame-oss
licence_source: MIT
dépend_de: [P04, P10, P11]
mise_a_jour: 2026-10-31
---

# Simulateur de négociation contractuelle

## 1. Origine

Wargame fait négocier un contrat par deux agents, l'un du côté de l'utilisateur, l'autre adverse. Après import d'un .docx, un pipeline extrait les parties et les points négociables ; l'utilisateur choisit son camp, donne des consignes à chaque agent et fixe la taille de la simulation (nombre de points, nombre de tours). Les agents négocient point par point, un détecteur décide quand une position est réellement acceptée, et les clauses convenues sont compilées dans un .docx avec modifications suivies. L'utilisateur fournit sa clé OpenAI ou Anthropic. L'outil se présente comme un moyen de tester des positions, pas comme un avis juridique. Consulté le 2026-10-31.

## 2. Problème ou opportunité

Préparer une négociation demande d'anticiper les objections de l'autre partie. Un jeune avocat a rarement l'occasion de s'y exercer.

## 3. Solution envisagée

Version locale : import d'un contrat, extraction des points, simulation avec affichage en direct, rapport des positions et des concessions.

Hors périmètre de la première version : production d'un .docx avec modifications suivies (dépend de P04), comptes utilisateurs, partage.

## 4. Adaptation à jerlash.labs

L'original repose sur un serveur (Next.js, Supabase, Vercel Workflows, authentification, clé stockée chiffrée). Cette architecture est contraire à ADR-004. Il faut une version qui tourne en local, sans base de données distante. Le code source est sous MIT et peut servir de référence pour les prompts, la boucle de supervision et le détecteur de résolution.

## 5. Approche technique pressentie

Application locale (page HTML hors ligne ou application Node lancée en local), état en mémoire ou en fichier local. Plafonds de tours et de points obligatoires pour borner la dépense, comme dans l'original.

## 6. Contraintes et risques

Coût : une simulation complète consomme beaucoup d'appels ; afficher l'estimation avant lancement.
Déontologie : usage pédagogique et préparatoire ; ne pas présenter le résultat comme une prévision.
Licence : MIT, mention de copyright à conserver pour tout code repris.

## 7. Critères d'acceptation

- [ ] Simulation de trois points en moins de [À FIXER] euros sur le jeu de test.
- [ ] Aucun flux réseau autre que vers le fournisseur choisi.
- [ ] Transcription exportable.

## 8. Appétit

[À COMPLÉTER]

## 9. Questions ouvertes

1. Intérêt pour un usage de formation (stagiaires) plutôt que de production ?

## 10. Prochaine étape

Lire docs/architecture.md de wargame-oss et identifier ce qui est réutilisable en local.
