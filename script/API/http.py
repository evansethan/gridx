from pathlib import Path
import httpx

CACHE_DIR = Path(__file__).parent / "_cache"
ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyz1234567890%+,^=._")

class FetchException(Exception):
    """
    Turn a httpx.Response into an exception.
    """

    def __init__(self, response: httpx.Response):
        super().__init__(
            f"{response.status_code} retrieving {response.url}: {response.text}"
        )

def url_to_cache_key(url: str) -> str:
    """
    Convert a URL to a cache key that can be stored on disk.

    The rules are as follows:

    1) All keys should be lower case. URLs are case-insensitive.
    2) The leading http(s):// should be removed.
    3) The remaining characters should all be in ALLOWED_CHARS.
       Any other characters should be converted to `_`.

    This lets us have unique filenames that are safe to write to disk.
    Some characters (notably `/`) would cause problems if not removed.
    """
    newrl = url.lower()
    if newrl.startswith("http://"):
        newrl = newrl.removeprefix("http://")
    if newrl.startswith("https://"):
        newrl = newrl.removeprefix("https://")
    
    newrl_set = set(newrl)
    char_to_remove = newrl_set.difference(ALLOWED_CHARS)

    for char in char_to_remove:
        newrl = newrl.replace(char, '_')

    return newrl

def cached_get(url, offset) -> dict:
    """
    This function caches all GET requests it makes, by writing
    the successful responses to disk. This API does not require an API key,
    so there is no concern about having to protect an API key.

    Parameters:
        url:        Base URL to visit.
        offset:     Record offset

    Returns:
        Contents of response as text.

    Raises:
        FetchException if a non-200 response occurs.
    """
    api_url = url + str(offset)
    cache_key = url_to_cache_key(api_url)
    file_path = CACHE_DIR / cache_key

    if file_path.exists():
        #text of the response should be returned
        f = file_path.read_text()
        return f
    else:
        #make the request
        response = httpx.get(api_url, follow_redirects=True)
        if response.status_code == 200:
            #create directory if doesn't exist
            CACHE_DIR.mkdir(exist_ok=True)
            #write it to the disc using a path
            file_path.write_text(response.text)
            #text of the response should be returned
            return response.text
        else: #(we don't have it and the request was not successful)
            raise FetchException(response)
