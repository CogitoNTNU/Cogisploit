"""Refresh the bundled PokéAPI data and artwork (run manually, not on page loads)."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

ROOT = Path(__file__).parent
IDS = (6, 9, 25, 65, 94, 129, 130, 143, 149, 150, 248, 376, 384, 445)


def fetch(species):
    def get(url):
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response

    pokemon = get(f"https://pokeapi.co/api/v2/pokemon/{species}").json()
    info = get(f"https://pokeapi.co/api/v2/pokemon-species/{species}").json()
    entry = next(e["flavor_text"] for e in info["flavor_text_entries"] if e["language"]["name"] == "en")
    image = pokemon["sprites"]["other"]["official-artwork"]["front_default"] or pokemon["sprites"]["front_default"]
    target = ROOT / "static" / "pokemon" / f"{species}.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(get(image).content)
    return dict(id=species, name=pokemon["name"].capitalize(),
                type="/".join(t["type"]["name"].capitalize() for t in pokemon["types"]),
                stats=sum(s["base_stat"] for s in pokemon["stats"]),
                entry=" ".join(entry.split()), source=f"https://pokeapi.co/api/v2/pokemon-species/{species}/",
                artwork_source=image)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(fetch, IDS))
    (ROOT / "pokedex.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"Cached {len(rows)} Pokédex entries and images from PokéAPI.")
