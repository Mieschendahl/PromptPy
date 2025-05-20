import shutil
import hashlib
import string
import random
from pathlib import Path
from typing import Optional

def pad(text: str, padding: str = "  ") -> str:
    """Adds a given padding to the left of each line.
    
    Args:
        text: The string to pad.
        padding: The padding to add.
    
    Returns:
        padded: The padded string.
    """
    return "\n".join(f"{padding}{line}" for line in text.split("\n"))

def hash_str(text: str, length: int = 16) -> str:
    """Hashes a given string into a fixed size hash.
    
    Args:
        text: The string to hash.
        length: The size of the hash.
        
    Returns:
        hash: The hashed string.
    """
    return hashlib.blake2b(text.encode(), digest_size=length).hexdigest()

def random_str(length: int = 10, digits=True) -> str:
    """Generates a random lower case letters string.
    
    Args:
        length: The length of the generated string.
        
    Returns:
        The random string.
    """
    if digits:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def create_dir(dir_path: Path, src_path: Optional[Path] = None, remove: bool = True) -> None:
    """Creates a directory at the given path, including parent directories.

    Args:
        dir_path: The path where the directory should be created.
        src_path: If src_path is not None, then copy the content from src_path to dir_path.
        remove: If an existing directory at dir_path should first be removed.
    """
    if remove:
        shutil.rmtree(dir_path, ignore_errors=True)
    if src_path is None:
        dir_path.mkdir(parents=True, exist_ok=True)
    else:
        shutil.copytree(src_path, dir_path, dirs_exist_ok=True) 

def load_text(file_path: Path) -> Optional[str]:
    """Loads text from cache.
    
    Args:
        file_path: The path of the file.
        
    Returns:
        text: The loaded text, or None.
    """
    if file_path.is_file():
        return file_path.read_text()
    return None

def save_text(file_path: Path, text: Optional[str]):
    """Stores a given text into cache.
    
    Args:
        file_path: The path of the file.
        text: The text to save, or None if the file should be removed.
    """
    file_path = file_path
    if text is None:
        if file_path.is_file():
            file_path.unlink()
    else:
        create_dir(file_path.parent, remove=False)
        file_path.write_text(text)