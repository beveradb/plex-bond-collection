# Plex James Bond Collection Creator

Automatically create a collection of all James Bond movies in your Plex library.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Plex Token

You need your Plex authentication token. Here are a few ways to get it:

#### Option A: Via Web Interface
1. Open any movie in your Plex web interface (https://plex.beveradb.com)
2. Click the three dots ⋯ and select "Get Info"
3. Click "View XML" at the bottom
4. Look at the URL - your token is the value after `?X-Plex-Token=`

#### Option B: Via Browser Console
1. Open your Plex web interface
2. Press F12 to open browser console
3. Type: `localStorage.getItem('myPlexAccessToken')`
4. Copy the token (without quotes)

#### Option C: Via Plex Settings
1. Go to https://app.plex.tv/desktop/#!/settings/account
2. Enable "Show Advanced" at the bottom
3. Your token will be shown

### 3. Run the Script

```bash
# Set your Plex token as an environment variable
export PLEX_TOKEN='your-plex-token-here'

# Run the script
python create_bond_collection.py
```

### 4. Optional Configuration

You can customize the script with environment variables:

```bash
# Change the server URL (default: https://plex.beveradb.com)
export PLEX_URL='https://your-plex-server.com'

# Change the library name (default: Movies)
export PLEX_LIBRARY='My Movies'

# Change the collection name (default: James Bond)
export COLLECTION_NAME='007 Collection'

# Run with custom settings
python create_bond_collection.py
```

## What the Script Does

1. **Connects to your Plex server** using the provided URL and token
2. **Searches for James Bond movies** using multiple strategies:
   - Title searches for "James Bond", "007", and "Bond"
   - Optional actor searches for Bond actors (Connery, Moore, Craig, etc.)
3. **Creates a collection** named "James Bond" (or your custom name)
4. **Adds all found movies** to the collection
5. **Shows you the results** with a summary of what was added

## Features

- ✅ Automatic detection of Bond movies in your library
- ✅ Handles duplicate detection (won't add same movie twice)
- ✅ Updates existing collections (adds new movies if you run it again)
- ✅ Works with any Plex server (local or remote)
- ✅ Customizable library and collection names
- ✅ Detailed output showing what was found and added

## Troubleshooting

### "Library 'Movies' not found"
Your movie library might have a different name. The script will show you all available libraries. Use the `PLEX_LIBRARY` environment variable to specify the correct one.

### "No James Bond movies found"
Make sure:
- Your Bond movies are properly named with "James Bond", "007" or the specific title in Plex
- The movies have been scanned and matched with metadata from TheMovieDB or IMDb
- Try running a "Scan Library Files" and "Refresh Metadata" on your Movies library first

### "Failed to connect to Plex server"
Check that:
- Your server URL is correct
- Your Plex server is running and accessible
- Your token is valid
- If using a remote connection, your server is published and accessible externally

## Accessing Your Collection

After the script runs successfully, you can find your collection:

1. Open your Plex web interface
2. Go to your Movies library
3. Look for "Collections" in the sidebar (or at the top)
4. Find "James Bond" collection
5. You can pin it to your home screen or customize it further

## Advanced Usage

### Run Without Environment Variables

Edit the script and add your token directly (line ~139):

```python
token = 'your-token-here'  # Replace with your actual token
```

### Modify Search Logic

The script searches for movies by title and optionally by actor. You can modify the search terms in the `create_bond_collection()` function around line 43.

## API Documentation

This script uses the [PlexAPI Python library](https://github.com/pkkid/python-plexapi) which wraps the official [Plex Media Server API](https://developer.plex.tv/pms/).

## Security Note

⚠️ **Your Plex token is like a password** - keep it secure! Don't commit it to version control or share it publicly.
