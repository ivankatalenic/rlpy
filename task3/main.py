from time import sleep
from random import uniform
from datetime import timedelta, datetime, timezone

from cache import cache

@cache(expiration=timedelta(seconds=10), max_uses=5)
def fun(*, a=1,b=2,c=2):
	print("fun called")
	return (a,b,c)

def main(args: list[str]) -> int:
	for i in range(20):
		now = datetime.now(timezone.utc)
		print(f"{i}, {now}: {fun()}")
		sleep(uniform(0.01, 2.))
	return 0

if __name__ == "__main__":
	import sys
	sys.exit(main(sys.argv))
