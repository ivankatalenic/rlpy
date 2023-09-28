from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

def cache(max_uses: int = 10, expiration: timedelta = timedelta(minutes=5)):
	"""
	A decorator that caches function calls.
	
	A function call with the given arguments can be reused
	up to `max_uses` times or for a time period `expiration`,
	whichever happens first.

	All arguments to the function must be hashable.

	The old cached function calls aren't cleaned automatically,
	and this may cause a memory leak in long-running applications.

	Not designed for concurrent use even if the decorated function is.
	"""
	if not isinstance(max_uses, int):
		raise TypeError("the max_uses argument must be an integer")
	if max_uses < 1:
		raise ValueError("the max_uses argument can't be less than 1")
	if not isinstance(expiration, timedelta):
		raise TypeError("the expiration argument must be a timedelta")
	if expiration < timedelta(seconds=0):
		raise ValueError("the expiration period argument can't be negative")
	
	def cache_inner(fun):
		@dataclass
		class CacheEntry:
			value: object
			use_count: int
			created_at: datetime
		
		cache: dict[tuple, CacheEntry] = dict()

		def cached_fun(*args, **kwargs):
			cache_arg = (args, tuple(kwargs.items()))
			now = datetime.now(timezone.utc)
			if cache_arg not in cache \
					or (entry := cache[cache_arg]).use_count >= max_uses \
					or entry.created_at < now - expiration:
				value = fun(*args, **kwargs)
				cache[cache_arg] = CacheEntry(value, 1, now)
				return value
			entry.use_count += 1
			return entry.value
		
		return cached_fun
	
	return cache_inner
