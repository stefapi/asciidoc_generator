#!/usr/bin/env python3
"""
asc_tree.py – Affiche les dépendances Asciidoctor (include::).

Usage :
    python asc_tree.py [OPTIONS] [CHEMIN_RACINE]

Options :
    -r, --reverse   Pour chaque fichier, afficher qui l’inclut (vue inverse).
"""

from pathlib import Path
from collections import defaultdict
import argparse
import re
import sys

# Détecte :  include::chemin[ ...
INCLUDE_RE = re.compile(r'^\s*include::([^\[]+)\[')

# ---------------------------------------------------------------------------
# Collecte des dépendances
# ---------------------------------------------------------------------------
def collect_dependencies(root: Path):
    """
    Explore `root` et renvoie un dict :
        { fichier_absolu : [fichiers inclus] }
    Les fichiers sans include sont quand même présents (valeur liste vide).
    """
    deps = defaultdict(list)
    for adoc in root.rglob("*.asc"):
        abs_path = str(adoc.resolve())
        deps[abs_path]                      # → clé assurée, même sans include
        for line in adoc.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = INCLUDE_RE.match(line)
            if m:
                deps[abs_path].append(str((adoc.parent / m.group(1)).resolve()))
    return deps

def invert_dependencies(deps):
    """Construit le mapping inverse : enfant -> [parents]."""
    parents = defaultdict(list)
    for parent, children in deps.items():
        for child in children:
            parents[child].append(parent)
    for f in deps:                          # assure que chaque fichier est clé
        parents[f]
    return parents

# ---------------------------------------------------------------------------
# Détermination des racines / feuilles
# ---------------------------------------------------------------------------
def roots(deps):
    included = {inc for lst in deps.values() for inc in lst}
    return [f for f in deps if f not in included] or list(deps.keys())

# ---------------------------------------------------------------------------
# Affichage arborescent (style `tree`)
# ---------------------------------------------------------------------------
def _print_tree(node, mapping, prefix="", is_tail=True, visited=None):
    if visited is None:
        visited = set()
    rel = Path(node).relative_to(Path.cwd())
    connector = "└── " if is_tail else "├── "
    print(f"{prefix}{connector}{rel}{'  (cycle)' if node in visited else ''}")

    if node in visited:
        return
    visited.add(node)

    children = mapping.get(node, [])
    for i, child in enumerate(children):
        last = i == len(children) - 1
        _print_tree(child, mapping,
                    prefix + ("    " if is_tail else "│   "),
                    last, visited)

# ---------------------------------------------------------------------------
# Deux vues possibles
# ---------------------------------------------------------------------------
def print_normal_view(deps):
    """Vue classique : racines → inclus."""
    for r in roots(deps):
        print(Path(r).relative_to(Path.cwd()))
        for i, child in enumerate(deps.get(r, [])):
            _print_tree(child, deps, "", i == len(deps[r]) - 1)

def print_reverse_view(deps):
    """Vue inverse : pour chaque fichier, qui l’inclut (chaîne ascendante)."""
    parents = invert_dependencies(deps)
    for f in sorted(deps):                  # tri alphabétique pour la lisibilité
        rel = Path(f).relative_to(Path.cwd())
        print(rel)
        plist = parents.get(f, [])
        for i, p in enumerate(plist):
            _print_tree(p, parents, "", i == len(plist) - 1)

# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Affiche l’arbre des directives include:: d’Asciidoctor")
    parser.add_argument("root", nargs="?", default=".",
                        help="Répertoire racine (défaut : courant)")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="Affiche, pour chaque fichier, qui l’inclut")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        sys.exit(f"Erreur : {root} n’est pas un répertoire.")

    deps = collect_dependencies(root)
    if not deps:
        sys.exit("Aucun fichier .asc trouvé.")

    if args.reverse:
        print_reverse_view(deps)
    else:
        print_normal_view(deps)

if __name__ == "__main__":
    main()
