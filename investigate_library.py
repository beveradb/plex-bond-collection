#!/usr/bin/env python3
"""
Script to investigate what Bond movies are in the Plex library
"""

from plexapi.server import PlexServer
import os

# Known James Bond movie titles
ALL_BOND_MOVIES = [
    "Dr. No",
    "From Russia with Love",
    "Goldfinger",
    "Thunderball",
    "You Only Live Twice",
    "On Her Majesty's Secret Service",
    "Diamonds Are Forever",
    "Live and Let Die",
    "The Man with the Golden Gun",
    "The Spy Who Loved Me",
    "Moonraker",
    "For Your Eyes Only",
    "Octopussy",
    "A View to a Kill",
    "The Living Daylights",
    "Licence to Kill",
    "GoldenEye",
    "Tomorrow Never Dies",
    "The World Is Not Enough",
    "Die Another Day",
    "Casino Royale",
    "Quantum of Solace",
    "Skyfall",
    "Spectre",
    "No Time to Die",
]

baseurl = os.environ.get('PLEX_URL', 'https://plex.beveradb.com')
token = os.environ.get('PLEX_TOKEN', '')

if not token:
    print("ERROR: PLEX_TOKEN environment variable is required!")
    print("Run: export PLEX_TOKEN='your-token-here'")
    exit(1)

print("Connecting to Plex...")
plex = PlexServer(baseurl, token)
movies = plex.library.section('Movies')

print(f"\nTotal movies in library: {len(movies.all())}")

print("\n" + "="*70)
print("SEARCHING FOR KNOWN BOND MOVIE TITLES")
print("="*70)

found_movies = []
not_found = []

for bond_title in ALL_BOND_MOVIES:
    results = movies.search(title=bond_title)
    if results:
        print(f"✓ FOUND: {bond_title}")
        for result in results:
            print(f"    → {result.title} ({result.year})")
            found_movies.append(result)
    else:
        not_found.append(bond_title)

print(f"\n{'='*70}")
print(f"SUMMARY")
print(f"{'='*70}")
print(f"Found: {len(found_movies)} Bond movies")
print(f"Not found: {len(not_found)} Bond movies")

if not_found:
    print(f"\nMissing from library:")
    for title in not_found:
        print(f"  - {title}")

print("\n" + "="*70)
print("TESTING SEARCH METHODS")
print("="*70)

# Test different search approaches
test_searches = [
    ("title='James Bond'", lambda: movies.search(title="James Bond")),
    ("title='007'", lambda: movies.search(title="007")),
    ("title='Bond'", lambda: movies.search(title="Bond")),
    ("search('Bond')", lambda: movies.search("Bond")),
    ("search('007')", lambda: movies.search("007")),
]

for desc, search_func in test_searches:
    try:
        results = search_func()
        print(f"\n{desc}: Found {len(results)} results")
        for r in results[:5]:  # Show first 5
            print(f"  - {r.title} ({r.year})")
        if len(results) > 5:
            print(f"  ... and {len(results) - 5} more")
    except Exception as e:
        print(f"\n{desc}: ERROR - {e}")

print("\n" + "="*70)
print("CHECKING MOVIE METADATA")
print("="*70)

# Check the metadata of movies we found
if found_movies:
    sample = found_movies[0]
    print(f"\nSample movie: {sample.title}")
    print(f"  Year: {sample.year}")
    print(f"  Summary: {sample.summary[:100] if sample.summary else 'N/A'}...")
    print(f"  Collections: {[c.tag for c in sample.collections]}")
    print(f"  Genres: {[g.tag for g in sample.genres]}")
    
    # Check if there's already a Bond collection in metadata
    if sample.collections:
        print(f"\n  ⚠️  This movie already has collection metadata!")
