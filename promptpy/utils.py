import sys
import shutil
import hashlib
import string
import random
from pathlib import Path
from typing import Any, Optional, TextIO

_log: Optional[TextIO] = sys.stdout

def set_log_file(log: Optional[TextIO]) -> None:
    """Set the file object to which the conversation between prompter and model is saved to.
    If stream is None, then no logs are made."""
    global _log
    _log = log

def get_log_file() -> Optional[TextIO]:
    return _log

def log(*texts: str, enclose: Optional[str] = None, **kwargs: Any) -> None:
    """Costum logging function, with special formating arguments."""
    if _log is None:
        return None
    
    output = []
    for text in texts:
        lines = str(text).split("\n")
        text = "\n".join(lines)
        if enclose is not None:
            text = enclose + " " + text + " " + enclose
        output.append(text)
    if enclose is not None:
        print(enclose * len(output[-1]), file=_log)
    print(*output, file=_log, **kwargs)
    if enclose is not None:
        print(enclose * len(output[-1]), file=_log)

def pad(string: str, padding: str = "  ") -> str:
    """Adds a given padding to the left of each line."""
    return "\n".join(f"{padding}{line}" for line in string.split("\n"))

def hash_str(string: str, length: int = 16) -> str:
    """Hashes a given string into a fixed size hash."""
    return hashlib.blake2b(string.encode(), digest_size=length).hexdigest()

def random_str(length: int = 16, digits: bool = False):
    """Generates a random lower case letters string. If digits is true, the string will also contain digits."""
    if digits:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def create_dir(dir_path: Path, src_path: Optional[Path] = None, remove: bool = True) -> None:
    """Creates a directory at the given path, including parent directories.

    Args:
        dir_path: The path where the directory should be created.
        src_path: Copies from src_path if not None.
        remove: If True, removes the directory if it already exists.
    """
    if remove:
        shutil.rmtree(dir_path, ignore_errors=True)
    if src_path is None:
        dir_path.mkdir(parents=True, exist_ok=True)
    else:
        shutil.copytree(src_path, dir_path, dirs_exist_ok=True) 
        
_use_cache: bool = True

def set_use_cache(use_cache: bool) -> None:
    """Set whether cache should be used."""
    global _use_cache
    _use_cache = use_cache

def get_use_cache() -> bool:
    return _use_cache

_cache_tag: Any = "#DEFAULT#"

def set_cache_tag(cache_tag: Any) -> None:
    """Set a cache tag to differentiate cache versions."""
    global _cache_tag
    _cache_tag = cache_tag

def get_cache_tag() -> Any:
    if _use_cache:
        return _cache_tag
    return "#TEMPORARY#"

_cache_path = Path("__promptpy__")

def load(file_path: Path) -> Optional[str]:
    """Loads text from cache, if it exists.
    
    Args:
        file_path: A relative file path.
    """
    if not _use_cache:
        return None
    assert not file_path.is_absolute(), "File path should be relative."
    file_path = _cache_path / file_path
    if file_path.is_file():
        return file_path.read_text()
    return None

def save(file_path: Path, text: Optional[str]) -> None:
    """Stores a given text into cache.
    
    Args:
        file_path: A relative file path.
        text: The text to save, or None if the file should be removed, if it exists.
    """
    if not _use_cache:
        return None
    assert not file_path.is_absolute(), "File path should be relative."
    file_path = _cache_path / file_path
    if text is None:
        if file_path.is_file():
            file_path.unlink()
    else:
        create_dir(file_path.parent, remove=False)
        file_path.write_text(text)

def clear_cache(cache_path: Path = Path()) -> None:
    """Clears cached data.

    Args:
        cache_path: The relative path to the cache subdirectory that should be cleared.
    """
    assert cache_path is None or not cache_path.is_absolute(), "Cache path should be relative."
    shutil.rmtree(_cache_path / cache_path, ignore_errors=True)