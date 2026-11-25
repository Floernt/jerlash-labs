"""Chargement des skills (skills/<nom>/SKILL.md) et du registre des sources.

Un skill est un fichier du dépôt : en-tête (nom, version, statut, dernière
relecture juridique, sources, schéma de sortie), puis instructions. Le chargeur
refuse un skill dont l'en-tête est incomplet, dont une source n'est pas au
registre, ou qui se dit relu juridiquement sans date de relecture.

Dans le Lot 2, les deux skills sont `status: draft` et `last_legal_review: null` :
leur sortie porte toujours la mention « non vérifié juridiquement ».
"""

import json
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_SKILLS = os.path.join(RACINE, "skills")
REGISTRE = os.path.join(RACINE, "config", "registre-sources.json")
MARQUEUR_SKILL = "SKILL="
CHAMPS_REQUIS = {"name", "version", "status", "last_legal_review", "jurisdiction", "output_schema",
                 "max_action_level", "sources"}
STATUTS = {"draft", "reviewed"}
MENTION_NON_VERIFIE = "Skill en brouillon, non vérifié juridiquement : sortie à relire par un avocat."


class SkillInvalide(ValueError):
    pass


def _valeur(brut: str):
    brut = brut.strip()
    if brut == "null":
        return None
    if brut.startswith("[") and brut.endswith("]"):
        return [x.strip() for x in brut[1:-1].split(",") if x.strip()]
    return brut


def lire_entete(texte: str) -> tuple[dict, str]:
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != "---":
        raise SkillInvalide("en-tête absent")
    try:
        fin = lignes.index("---", 1)
    except ValueError:
        raise SkillInvalide("en-tête non fermé") from None
    entete = {}
    for ligne in lignes[1:fin]:
        cle, sep, val = ligne.partition(":")
        if not sep:
            raise SkillInvalide(f"ligne d'en-tête illisible : {ligne!r}")
        entete[cle.strip()] = _valeur(val)
    return entete, "\n".join(lignes[fin + 1:]).strip()


def charger_registre(chemin: str = REGISTRE) -> dict:
    with open(chemin, encoding="utf-8") as f:
        return {s["id"]: s for s in json.load(f)["sources"]}


def charger(nom: str, registre: dict | None = None, dossier: str = DOSSIER_SKILLS) -> dict:
    """Renvoie le « skill bundle » transmis au runtime."""
    registre = registre if registre is not None else charger_registre()
    base = os.path.join(dossier, nom)
    with open(os.path.join(base, "SKILL.md"), encoding="utf-8") as f:
        entete, corps = lire_entete(f.read())
    manquants = CHAMPS_REQUIS - set(entete)
    if manquants:
        raise SkillInvalide(f"{nom} : champs manquants {sorted(manquants)}")
    if entete["name"] != nom:
        raise SkillInvalide(f"{nom} : nom incohérent avec le dossier")
    if entete["status"] not in STATUTS:
        raise SkillInvalide(f"{nom} : statut inconnu")
    if entete["status"] == "reviewed" and not entete["last_legal_review"]:
        raise SkillInvalide(f"{nom} : relu sans date de relecture")
    inconnues = [s for s in entete["sources"] if s not in registre]
    if inconnues:
        raise SkillInvalide(f"{nom} : sources absentes du registre {inconnues}")
    with open(os.path.join(base, entete["output_schema"]), encoding="utf-8") as f:
        schema = json.load(f)
    verifie = entete["status"] == "reviewed" and bool(entete["last_legal_review"])
    sources = [{"id": s, "titre": registre[s]["titre"], "statut": registre[s]["statut"]}
               for s in entete["sources"]]
    instructions = (f"{MARQUEUR_SKILL}{nom}\n{corps}\n\n"
                    "Réponds uniquement par un objet JSON conforme au schéma de sortie suivant : "
                    + json.dumps(schema, ensure_ascii=False, sort_keys=True) + " "
                    "Sources disponibles (identifiant, statut) : "
                    + ", ".join(f"{s['id']} ({s['statut']})" for s in sources) + ".")
    return {"nom": nom, "version": entete["version"], "status": entete["status"],
            "last_legal_review": entete["last_legal_review"], "verifie_juridiquement": verifie,
            "max_action_level": entete["max_action_level"], "sources": sources,
            "schema_sortie": schema, "instructions": instructions,
            "mention": None if verifie else MENTION_NON_VERIFIE}


def lister(dossier: str = DOSSIER_SKILLS) -> list[str]:
    return sorted(n for n in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, n, "SKILL.md")))
