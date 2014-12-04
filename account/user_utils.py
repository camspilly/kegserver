from random import randint

def generatepin(n):
  range_start = 10**(n-1)
  range_end = (10**n)-1
  return randint(range_start, range_end)
