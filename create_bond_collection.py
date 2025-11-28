#!/usr/bin/env python3
"""
Script to create a James Bond collection in Plex
"""

from plexapi.server import PlexServer
from plexapi.exceptions import NotFound
import os
import sys


def create_bond_collection(baseurl, token, library_name="Movies", collection_name="James Bond"):
    """
    Create a James Bond collection in Plex
    
    Args:
        baseurl: URL to your Plex server (e.g., 'https://plex.beveradb.com')
        token: Your Plex authentication token
        library_name: Name of your movie library (default: "Movies")
        collection_name: Name for the collection (default: "James Bond")
    """
    
    # Complete list of all official James Bond movies
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
        # Add non-Eon productions if desired
        "Casino Royale (1967)",  # Spoof version
        "Never Say Never Again",  # Non-Eon Connery film
    ]
    
    print(f"Connecting to Plex server at {baseurl}...")
    try:
        plex = PlexServer(baseurl, token)
        print(f"✓ Connected to: {plex.friendlyName}")
    except Exception as e:
        print(f"✗ Failed to connect to Plex server: {e}")
        sys.exit(1)
    
    # Get the movie library
    print(f"\nSearching for library: {library_name}...")
    try:
        movies = plex.library.section(library_name)
        print(f"✓ Found library: {movies.title}")
        print(f"  Total movies in library: {len(movies.all())}")
    except NotFound:
        print(f"✗ Library '{library_name}' not found!")
        print("\nAvailable libraries:")
        for section in plex.library.sections():
            print(f"  - {section.title} (type: {section.type})")
        sys.exit(1)
    
    # Search for James Bond movies by known titles
    print(f"\nSearching for James Bond movies by title...")
    print(f"  Checking {len(ALL_BOND_MOVIES)} known Bond movie titles...")
    
    bond_movies = []
    found_titles = set()
    not_found = []
    
    for bond_title in ALL_BOND_MOVIES:
        results = movies.search(title=bond_title)
        if results:
            for movie in results:
                if movie.title not in found_titles:
                    bond_movies.append(movie)
                    found_titles.add(movie.title)
                    print(f"  ✓ Found: {movie.title} ({movie.year})")
        else:
            not_found.append(bond_title)
    
    print(f"\n{'='*70}")
    print(f"SEARCH RESULTS")
    print(f"{'='*70}")
    print(f"✓ Found {len(bond_movies)} Bond movies in your library")
    
    if not_found:
        print(f"\nℹ️  {len(not_found)} Bond movies not in your library:")
        for title in not_found:
            print(f"  - {title}")
    
    if not bond_movies:
        print("\n✗ No James Bond movies found in your library!")
        sys.exit(1)
    
    # Create or update the collection
    print(f"\nCreating/updating collection: {collection_name}...")
    
    try:
        # Check if collection already exists
        existing_collections = movies.collections()
        existing_collection = None
        for coll in existing_collections:
            if coll.title == collection_name:
                existing_collection = coll
                break
        
        if existing_collection:
            print(f"  Collection '{collection_name}' already exists")
            print(f"  Current items in collection: {len(existing_collection.items())}")
        
        # Add movies to collection
        added_count = 0
        for movie in bond_movies:
            try:
                # Add to collection by editing the movie's collection field
                current_collections = [c.tag for c in movie.collections]
                if collection_name not in current_collections:
                    movie.addCollection(collection_name)
                    added_count += 1
                    print(f"  ✓ Added: {movie.title}")
                else:
                    print(f"  - Already in collection: {movie.title}")
            except Exception as e:
                print(f"  ✗ Failed to add {movie.title}: {e}")
        
        print(f"\n✓ Collection '{collection_name}' created/updated!")
        print(f"  Total movies added: {added_count}")
        print(f"  Total movies in collection: {len(bond_movies)}")
        print(f"\nYou can now find your collection at:")
        print(f"  {baseurl}/web/index.html#!/server/{plex.machineIdentifier}/details?key=%2Flibrary%2Fcollections%2F")
        
    except Exception as e:
        print(f"✗ Failed to create collection: {e}")
        sys.exit(1)


def get_plex_token_instructions():
    """Print instructions on how to get a Plex token"""
    print("\n" + "="*70)
    print("HOW TO GET YOUR PLEX TOKEN")
    print("="*70)
    print("\nOption 1 - Via Web Interface:")
    print("  1. Open any item in your Plex web interface")
    print("  2. Click 'Get Info' or the (i) icon")
    print("  3. Click 'View XML' at the bottom")
    print("  4. Look at the URL - your token is after '?X-Plex-Token='")
    print("\nOption 2 - Via Account Settings:")
    print("  1. Go to https://app.plex.tv/desktop/#!/settings/account")
    print("  2. Scroll down and enable 'Show Advanced'")
    print("  3. At the bottom right, you'll see your token")
    print("\nOption 3 - Via Browser Console:")
    print("  1. Open your Plex web interface")
    print("  2. Open browser console (F12)")
    print("  3. Type: localStorage.getItem('myPlexAccessToken')")
    print("="*70 + "\n")


def main():
    print("="*70)
    print("PLEX JAMES BOND COLLECTION CREATOR")
    print("="*70)
    
    # Get configuration from environment variables or prompt
    baseurl = os.environ.get('PLEX_URL', 'https://plex.beveradb.com')
    token = os.environ.get('PLEX_TOKEN', '')
    
    if not token:
        print("\n⚠️  No Plex token found!")
        get_plex_token_instructions()
        
        print("Please set your Plex token as an environment variable:")
        print("  export PLEX_TOKEN='your-token-here'")
        print("\nOr edit this script and add it directly.")
        print("\nOptionally, you can also set:")
        print("  export PLEX_URL='https://your-plex-url.com'")
        sys.exit(1)
    
    # Allow overriding library and collection names
    library_name = os.environ.get('PLEX_LIBRARY', 'Movies')
    collection_name = os.environ.get('COLLECTION_NAME', 'James Bond')
    
    print(f"\nConfiguration:")
    print(f"  Server URL: {baseurl}")
    print(f"  Library: {library_name}")
    print(f"  Collection: {collection_name}")
    print(f"  Token: {'*' * 10}...{token[-4:]}")
    
    create_bond_collection(baseurl, token, library_name, collection_name)


if __name__ == "__main__":
    main()
