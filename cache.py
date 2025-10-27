"""Document caching functionality."""

import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any


class DocumentCache:
    """Simple file-based cache for documentation with TTL support."""
    
    def __init__(self, cache_dir: str = ".doc_cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata from disk."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_metadata(self):
        """Save cache metadata to disk."""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception:
            pass
    
    def _get_cache_key(self, url: str) -> str:
        """Generate a unique cache key from URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get(self, url: str) -> str | None:
        """Retrieve cached content if valid, else None."""
        cache_key = self._get_cache_key(url)
        
        if cache_key in self.metadata:
            cached_at = datetime.fromisoformat(self.metadata[cache_key]['cached_at'])
            if datetime.now() - cached_at < self.ttl:
                cache_file = self.cache_dir / f"{cache_key}.txt"
                if cache_file.exists():
                    try:
                        with open(cache_file, 'r', encoding='utf-8') as f:
                            return f.read()
                    except Exception:
                        pass
        return None
    
    def set(self, url: str, content: str):
        """Store content in cache with metadata."""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{cache_key}.txt"
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.metadata[cache_key] = {
                'url': url,
                'cached_at': datetime.now().isoformat(),
                'size': len(content)
            }
            self._save_metadata()
        except Exception:
            pass
    
    def clear_expired(self):
        """Remove expired cache entries."""
        expired_keys = []
        for cache_key, meta in self.metadata.items():
            cached_at = datetime.fromisoformat(meta['cached_at'])
            if datetime.now() - cached_at >= self.ttl:
                expired_keys.append(cache_key)
                cache_file = self.cache_dir / f"{cache_key}.txt"
                if cache_file.exists():
                    cache_file.unlink()
        
        for key in expired_keys:
            del self.metadata[key]
        
        if expired_keys:
            self._save_metadata()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_size = sum(meta.get('size', 0) for meta in self.metadata.values())
        return {
            'entries': len(self.metadata),
            'total_size_kb': total_size / 1024,
            'cache_dir': str(self.cache_dir)
        }