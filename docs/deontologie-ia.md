# Déontologie et IA distante : risques, limites et critères retenus par le projet

Date : 2026-11-01. Statut : document de travail, support de l'ADR-019 (qui remplace l'ADR-015). Il ne tranche pas à la place de l'avocat qui utilise un outil : l'usage de l'IA « relève de la liberté et de la responsabilité de l'avocat(e) » (AVOCATS.BE et OVB, p. 1).

Sources : `bibliotheque/fiches/AVOCATS-BE-OVB_lignes-directrices-ia.md` (texte belge, référence principale) et `bibliotheque/fiches/2026-03-13_CNB_deontologie-et-ia.md` (texte français, plus détaillé, éclairant mais non contraignant en Belgique). Matrice des fournisseurs : `docs/fournisseurs-ia.md`.

## 1. La règle de départ

Les lignes directrices belges posent deux règles distinctes, qu'il faut lire ensemble.

La première vise les données personnelles : « L'avocat(e) pseudonymise les données personnelles » et « s'abstient de saisir des données à caractère personnel dans les prompts, les entrées et/ou les autres documents qu'il/elle saisit dans les outils d'IA » (p. 2).

La seconde vise le secret : « L'avocat(e) ne communique jamais de documents ou d'informations couverts par le secret professionnel ou une obligation de confidentialité dans un outil d'IA. Une exception à ce principe s'applique uniquement si l'avocat est absolument certain qu'il/elle travaille dans un environnement fermé avec des garanties adéquates. » (p. 3)

La pseudonymisation répond à la première règle. Elle ne suffit pas toujours à sortir de la seconde : une pièce dont on a remplacé les noms reste un document du dossier, et ce qu'elle dit (la nature du litige, un montant, une chronologie, une stratégie) peut rester couvert par le secret. Le CNB le dit à sa manière : il faut rester « vigilant à l'identification rendue possible par le croisement de plusieurs données, quand bien même ces données auraient déjà été pseudonymisées » (p. 13).

## 2. Les risques propres à un envoi vers une API

1. Conservation par le fournisseur. Les fournisseurs conservent par défaut entrées et sorties pendant une durée qui va de 30 à 55 jours selon la matrice, pour la surveillance des abus. L'absence de conservation (ZDR) s'obtient sur demande, au cas par cas, et pas pour tous les modèles (`docs/fournisseurs-ia.md`, section 2).
2. Invérifiabilité. Ni l'avocat ni l'outil ne peuvent vérifier qu'un engagement de non-conservation ou de non-entraînement est respecté. Le CNB : cette assertion « n'est en général ni prouvable ni vérifiable » (p. 15). L'outil peut seulement afficher ce que l'utilisateur déclare dans sa configuration.
3. Lieu de traitement et droit applicable au prestataire. L'API directe d'Anthropic ne propose pas de traitement dans l'UE ; OpenAI, Mistral et Google Vertex AI en documentent un, sous conditions. Le CNB place en tête de ses critères le lieu d'hébergement et la nationalité du prestataire, en excluant les entreprises soumises à des lois extraterritoriales d'accès aux données (p. 15). Un point d'accès européen d'une société américaine ne règle pas ce second critère.
4. Pseudonymisation imparfaite. P09 Lite 0.1.0 a, sur le jeu de contrôle F-IDENT-01, un rappel de 63 % et ne trouve que 45 % des noms de personnes. Un envoi « après pseudonymisation par P09 » laisse donc partir, aujourd'hui, une partie importante des noms. Ce chiffre interdit de présenter la pseudonymisation automatique comme une garantie.
5. Réidentification par le contexte. Même un texte bien pseudonymisé peut désigner un client par recoupement (montant, nom de projet, style de rédaction ; CNB, p. 13).
6. Conflit d'intérêts et réutilisation entre dossiers. Le CNB demande de s'assurer que les données transmises ne puissent pas être réutilisées dans d'autres dossiers (p. 19).
7. Fiabilité. Le résultat d'un modèle doit être vérifié (AVOCATS.BE et OVB, p. 2). Pour P01, une proposition de rattachement ou de partie venant du modèle doit être marquée comme telle et rester « à vérifier ».

## 3. Ce que le projet entend par « environnement fermé avec des garanties adéquates »

Les lignes directrices belges ne définissent pas ces termes. La lecture suivante sert à informer l'avocat ; elle n'engage pas l'ordre et ne limite pas le choix du fournisseur (ADR-019).

Niveau 1, environnement fermé au sens strict : le modèle s'exécute sur la machine de l'avocat (ADR-010, mode C). Aucune donnée ne quitte le poste. C'est l'une des deux voies que le CNB cite pour « garantir l'étanchéité et la confidentialité » (p. 15). L'exception prévue par les lignes directrices belges peut alors s'appliquer sans dépendre d'un engagement d'un tiers.

Niveau 2, prestataire distant avec garanties contractuelles : l'avocat envoie des extraits à une API dont le fournisseur remplit les critères de la section 4. Ce n'est pas un environnement fermé au sens strict ; c'est l'avocat, et lui seul, qui juge si ces garanties sont « adéquates » pour le dossier en cause.

Niveau 3, prestataire distant qui ne remplit pas tous ces critères (pas de traitement dans l'UE, pas de ZDR, offre grand public). Les outils ne l'interdisent pas (ADR-019) ; l'écran d'envoi signale les critères manquants.

Dans les trois cas, l'outil n'envoie rien sans la décision explicite de l'avocat.

## 4. Grille d'information sur le prestataire

Depuis l'ADR-019, le choix du fournisseur est libre. Les critères suivants ne filtrent plus ; ils sont vérifiés sur la documentation officielle, datés dans `docs/fournisseurs-ia.md`, et affichés sur l'écran d'envoi :

1. offre payante ou professionnelle, sous conditions commerciales (pas d'offre grand public ni gratuite) ;
2. pas d'utilisation des entrées et sorties pour l'entraînement, par défaut et par contrat ;
3. absence de conservation (ZDR) disponible pour l'usage visé, ou à défaut durée de conservation courte et documentée, affichée à l'utilisateur ;
4. traitement dans l'UE documenté pour le point d'accès utilisé ;
5. contrat de sous-traitance conforme à l'article 28 du RGPD, avec liste des sous-traitants ultérieurs ;
6. pas de fonction avec état (fichiers déposés, traitements par lots, conversations conservées) dans l'usage qu'en fait l'outil.

La nationalité du prestataire (CNB, p. 15) est également affichée.

Sur la base de la matrice du 2026-10-31, et sous réserve des points `[À VÉRIFIER]` de sa section 6 :

| Fournisseur | Traitement UE documenté | ZDR | Société | Remplit la grille |
|---|---|---|---|---|
| Mistral AI, point d'accès `api.eu.mistral.ai` | Oui | Sur demande, offres payantes | Française | Oui, hors modèles « Preview » et « Labs » |
| Google Vertex AI, multirégion `eu` | Oui | Par configuration | Américaine | Oui |
| OpenAI, point d'accès Europe | Oui, sous condition de ZDR | Après approbation | Américaine | Oui, si ZDR déclaré |
| Anthropic, API directe | Non | Sur demande | Américaine | Non (critère 4) ; utilisable, avec signalement |
| Google, API Gemini (AI Studio) | Non documenté | Non | Américaine | Non (critères 3 et 4) ; utilisable, avec signalement |

## 5. Précautions communes à tout envoi

Elles valent pour le niveau 2, et pour le niveau 1 lorsque c'est pertinent :

1. le mode local sans IA reste le mode par défaut de chaque outil ;
2. seuls les extraits strictement nécessaires partent, jamais une pièce entière (CNB, p. 9 : limiter le contexte au strict nécessaire) ;
3. pseudonymisation locale avant l'envoi, avec affichage du texte qui va partir, pour que l'avocat corrige ce que P09 a manqué ;
4. écran d'envoi : fournisseur, point d'accès, lieu de traitement déclaré, nationalité du prestataire, conservation déclarée, coût estimé, case à cocher (`docs/fournisseurs-ia.md`, section 5.1) ;
5. chaque résultat venant du modèle est marqué comme tel et reste « à vérifier » ;
6. aucune journalisation du contenu envoyé ni de la clé.

## 6. Points que le projet ne tranche pas

- La question de savoir si un extrait pseudonymisé d'une pièce reste couvert par le secret professionnel dans un dossier donné.
- L'appréciation, par l'avocat, du caractère « adéquat » des garanties d'un prestataire distant.
- L'information du client : les lignes directrices belges n'imposent pas d'obligation générale (p. 2), mais la politique d'usage d'Anthropic, pour les domaines juridiques, demande d'informer la personne (`docs/fournisseurs-ia.md`, section 3.1).
- Les obligations RGPD de l'avocat (base de licéité, analyse d'impact, transferts) et celles qui pourraient découler du règlement (UE) 2024/1689.
