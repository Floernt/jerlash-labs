# AVOCATS.BE et OVB - Lignes directrices sur l'utilisation de l'intelligence artificielle

- Auteur : AVOCATS.BE et Orde van Vlaamse Balies (texte commun, version française et néerlandaise)
- Titre : « Lignes directrices à l'intention des avocat(e)s sur l'utilisation de l'intelligence artificielle » ; « Richtlijnen voor advocaten voor het gebruik van Artificiële Intelligentie »
- Date d'adoption : `[À VÉRIFIER]`
- URL officielle : `[À VÉRIFIER]`
- Fichier local : `sources/AVOCATS-BE-OVB_lignes-directrices-ia.pdf` (6 pages : FR p. 1 à 3, NL p. 4 à 6)
- Consulté le : 2026-11-01
- Portée : lignes directrices des deux ordres communautaires. Elles renvoient à l'article 455 du Code judiciaire et à l'article 1.2 du Code de déontologie d'AVOCATS.BE (article 1 du Codex OVB).

## Résumé

Résumé, pas une citation. L'usage de l'IA est libre et relève de la responsabilité de l'avocat. Celui-ci doit connaître les bases des LLM, lire les conditions d'utilisation de l'outil, vérifier le résultat et les sources, pseudonymiser les données personnelles, et ne jamais introduire d'information couverte par le secret professionnel dans un outil d'IA, sauf environnement fermé offrant des garanties adéquates. Pas d'obligation générale d'informer le client de l'usage de l'IA, mais obligation de signaler qu'un chatbot est un système d'IA. L'avocat reste responsable du résultat.

## Passages cités

« L'utilisation de l'IA n'est ni interdite ni obligatoire. L'utilisation de la technologie relève de la liberté et de la responsabilité de l'avocat(e). » (p. 1)

« L'avocat(e) examine attentivement les conditions d'utilisation de l'outil d'IA qu'il/elle souhaite utiliser. » Enjeux énumérés : « Conditions relatives à la formation, à la transmission et au stockage ; Conditions relatives au traitement ultérieur des données appliquées par la plateforme ; Localisation des opérations de traitement ; La nature ouverte ou fermée du système ; Conditions de responsabilité de la plateforme ; Les droits de propriété intellectuelle et les conditions d'octroi de licences. » (p. 2)

« L'avocat(e) vérifie le résultat, y compris les sources mentionnées. » (p. 2)

« L'avocat(e) n'a pas à communiquer sur l'utilisation qu'il/elle fait de l'IA, tout comme il/elle n'a pas à communiquer sur l'utilisation qu'il/elle fait d'autres applications informatiques. » (p. 2)

« L'avocat(e) pseudonymise les données personnelles. L'avocat(e) s'abstient de saisir des données à caractère personnel dans les prompts, les entrées et/ou les autres documents qu'il/elle saisit dans les outils d'IA. » (p. 2)

« Si le traitement des données personnelles est essentiel, l'avocat(e) est transparent(e) et demande le consentement de la personne concernée. » (p. 2)

« L'avocat(e) ne communique jamais de documents ou d'informations couverts par le secret professionnel ou une obligation de confidentialité dans un outil d'IA. Une exception à ce principe s'applique uniquement si l'avocat est absolument certain qu'il/elle travaille dans un environnement fermé avec des garanties adéquates. » (p. 3)

« Les avocats sont autorisés à développer des chatbots, mais les utilisateurs doivent comprendre et donc être informés qu'il s'agit d'un système d'IA automatisé. » (p. 3)

« L'avocat(e) reste toujours responsable en dernier ressort des résultats de l'IA qu'il/elle utilise. » (p. 3)

## Usage dans le projet

- Référence principale pour les outils qui envoient des données à une IA distante : ADR-015 (P01), `docs/deontologie-ia.md`.
- Les notions d'« environnement fermé » et de « garanties adéquates » ne sont pas définies par le texte. `docs/deontologie-ia.md` explique comment le projet les traduit en critères techniques, sans prétendre trancher à la place de l'avocat.
