from random import randint

def generatepin(n):
  range_start = 10**(n-1)
  range_end = (10**n)-1
  return randint(range_start, range_end)

def api_auth(key):
	return key == "1p_Msca+m$.idIpP7kn(cLf&9N5>3Q"