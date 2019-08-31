#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

import election_data
import square

def plot(D, leader_names, title, binwidth=0.25, aspect = 3, spacing = 0.2, **kwargs):
	wlbl, centers, h = square.histogram(D, leader_names, binwidth=binwidth, **kwargs)
	ht = np.sum(h, axis=1)
	ylog = int(np.ceil(np.log10(np.max(ht)))) - 1

	plt.suptitle(title, size=20, y=0.925, va='baseline')

	plt.plot(centers, ht / (10 ** ylog), linewidth=1)
	plt.xticks(np.arange(0, 101, 10))
	plt.ylim(bottom=0)
	plt.xlabel('Turnout %')
	plt.ylabel(wlbl)
	#ax.text(0.5, 0.5, f'$\\times 10^{{{ylog}}}$ {wlbl}\nin ${binwidth}\\,\\%$ bin', wrap=True, ha='center', va='center', transform=ax.transAxes)	# the \n is a hack to force good wrapping

if __name__ == '__main__':
	import os
	import argparse
	import matplotlib
	matplotlib.use('Agg')

	parser = argparse.ArgumentParser()
	parser.add_argument('data', nargs='?', metavar='DATA', default='https://github.com/schitaytesami/lab/releases/download/data-v2/RU_2018-03-18_president.tsv.gz', help='Data file to use')
	parser.add_argument('--bin-width', default=0.25, type=float, help='Bin width in percentage points')
	parser.add_argument('--weights', default='voters', choices={'voters', 'given', 'leader', 'ones'}, help="'ones' (counts polling stations), 'voters' (counts registered voters), 'given' (counts ballots given), or 'leader' (counts ballots for the leader)")
	parser.add_argument('--min-size', default=0, type=int, help='Minimum precinct size to include')
	parser.add_argument('--noise', action='store_true', help='Add U(-0.5,0.5) noise to the numerators (to remove division artifacts)')
	parser.add_argument('-o', '--output', default='turnout.png', help='Output file')
	args = parser.parse_args()

	D = election_data.load(args.data)

	plt.figure(figsize = (6, 2))
	plot(D, leader_names = election_data.RU_LEADER, title=os.path.basename(args.data), binwidth=args.bin_width, weights=args.weights, minsize=args.min_size, noise=args.noise)
	plt.savefig(args.output, bbox_inches='tight')
	plt.close()
