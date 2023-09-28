import unittest

from cache import cache
from datetime import timedelta

class TestCacheDecorator(unittest.TestCase):

	def test_call(self):
		is_called = False
		@cache(1, timedelta(seconds=1))
		def example():
			nonlocal is_called
			is_called = True
		example()
		self.assertTrue(is_called)
	
	def test_return_single_value(self):
		@cache(1, timedelta(seconds=1))
		def example():
			return 5
		self.assertEqual(example(), 5)

	def test_return_tuple_value(self):
		@cache(1, timedelta(seconds=1))
		def example():
			return 5, 6
		self.assertEqual(example(), (5, 6))
	
	def test_all_calls_cached(self):
		call_count = 0
		@cache(5, timedelta(seconds=1))
		def example():
			nonlocal call_count
			call_count += 1
		for _ in range(5):
			example()
		self.assertEqual(call_count, 1)
	
	def test_all_calls_not_cached(self):
		call_count = 0
		@cache(1, timedelta(seconds=1))
		def example():
			nonlocal call_count
			call_count += 1
		for _ in range(5):
			example()
		self.assertEqual(call_count, 5)
	
	def test_some_calls_cached(self):
		call_count = 0
		@cache(5, timedelta(seconds=1))
		def example():
			nonlocal call_count
			call_count += 1
		for _ in range(9):
			example()
		self.assertEqual(call_count, 2)
	
	def test_different_args_cached(self):
		call_count: dict[int, int] = dict()
		@cache(5, timedelta(seconds=30))
		def example(arg: int):
			nonlocal call_count
			if arg in call_count:
				call_count[arg] += 1
			else:
				call_count[arg] = 1
		for _ in range(4):
			for i in range(3):
				example(i)
		self.assertDictEqual(call_count, {0: 1, 1: 1, 2: 1})
	
	def test_different_args_cache_refreshed(self):
		call_count: dict[int, int] = dict()
		@cache(5, timedelta(seconds=30))
		def example(arg: int):
			nonlocal call_count
			if arg in call_count:
				call_count[arg] += 1
			else:
				call_count[arg] = 1
		for _ in range(6):
			for i in range(3):
				example(i)
		self.assertDictEqual(call_count, {0: 2, 1: 2, 2: 2})
	
	# Much more tests remains to be added...

if __name__ == "__main__":
	unittest.main()
