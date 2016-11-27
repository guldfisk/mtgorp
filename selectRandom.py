import random
import sys
from loadCards import *

def main():
	random.seed()
	if len(sys.argv)<2: amnt = 1
	else: amnt = int(sys.argv[1])
	print(str([CardLoader.getSets()[key]['name'] for key in random.sample(list(CardLoader.getSets()), amnt)]))
	
if __name__=='__main__': main()