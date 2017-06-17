import random
import sys


def main():
	random.seed()
	if len(sys.argv)<2: amnt = 1
	else: amnt = int(sys.argv[1])
	print(str([CardLoader.get_sets()[key]['name'] for key in random.sample(list(CardLoader.get_sets()), amnt)]))
	
if __name__=='__main__': main()