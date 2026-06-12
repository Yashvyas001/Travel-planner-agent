"""
Places Service

Provides simple helpers to fetch popular/famous places for a destination using
the Wikipedia API as a free data source. Falls back to a curated list when
no results are found.
"""
import requests
from typing import List, Dict


WIKI_SEARCH_URL = 'https://en.wikipedia.org/w/api.php'


def search_wikipedia(query: str, limit: int = 5) -> List[Dict]:
    """Search Wikipedia and return top search results with titles and snippets."""
    try:
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json',
            'srlimit': limit
        }
        r = requests.get(WIKI_SEARCH_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        results = []
        for item in data.get('query', {}).get('search', []):
            results.append({
                'title': item.get('title'),
                'snippet': item.get('snippet')
            })
        return results
    except Exception:
        return []


def get_famous_places(destination: str, limit: int = 5) -> List[Dict]:
    """Return a list of famous places for the destination.

    Tries Wikipedia search for "<destination> attractions" then falls back
    to a short curated list.
    """
    query = f"{destination} attractions"
    results = search_wikipedia(query, limit)
    if results:
        return results

    # Fallback curated examples
    fallback = [
        {'title': f'{destination} Main Market', 'snippet': 'Popular market and gathering place.'},
        {'title': f'{destination} Old Town', 'snippet': 'Historic area with cultural sites.'},
        {'title': f'{destination} Beach', 'snippet': 'Sandy beach popular with tourists.'}
    ]
    return fallback


def get_viral_dhabas(destination: str) -> List[Dict]:
    """Attempt to find viral dhabas/eateries for the destination.

    Uses Wikipedia search for "famous dhabas in <destination>". Falls back to
    a small illustrative list.
    """
    query = f"famous dhabas in {destination}"
    results = search_wikipedia(query, limit=5)
    if results:
        # Map to dhaba-like structure
        return [{'name': r['title'], 'description': r['snippet'], 'location': destination} for r in results]

    # Fallback viral dhabas (illustrative)
    return [
        {'name': f'{destination} Highway Dhaba', 'description': 'Popular spot for travelers, famous for local food.', 'location': 'Near highway'},
        {'name': f'Grand Dhaba {destination}', 'description': 'Viral for its large portions and authentic flavours.', 'location': 'City outskirts'}
    ]
