#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

import election_data

def histogram(D, *, binwidth=0.25, minsize=0, seed=1):
	rnd = np.random.RandomState(seed)
	edges = np.arange(-binwidth/2, 100 + binwidth/2, binwidth)
	centers = np.arange(0, 100, binwidth)

	D = election_data.filter(D, ballots_valid_invalid_min=1, voters_registered_min=minsize, voters_voted_le_voters_registered=True, foreign=False)

	hs, ls = {}, {}
	for name in D.dtype.names:
		if not name.startswith('turnout_'): continue
		n = name[len('turnout_'):].replace('h', ':') 
		h = np.histogram(100 * D[name], bins=edges, weights=D.voters_registered * D[name])[0]
		hs[n] = h
		ls[n] = centers[np.argmax(h)], np.max(h)
	return centers, hs, ls

def plot(D, title, **kwargs):
	centers, hs, ls = histogram(D, **kwargs)
	binwidth = centers[1] - centers[0]

	plt.title(title + '\n')
	plt.xlabel('Turnout %')
	plt.ylabel('Ballots given in ${}\\,\\%$ bin'.format(binwidth))
	for time, h in hs.items():
		plt.plot(centers, h, linewidth=1, color='black')
	for time, l in ls.items():
		plt.text(l[0], l[1], time + '\n', ha='center', va='baseline')
	plt.xlim([0, 100])
	plt.ylim([0, plt.ylim()[1]])

if __name__ == '__main__':
	import os
	import argparse
	import matplotlib
	matplotlib.use('Agg')

	parser = argparse.ArgumentParser()
	parser.add_argument('data', nargs='?', metavar='DATA', default='https://github.com/schitaytesami/lab/releases/download/data-v2/2018.tsv.gz', help='Data file to use')
	parser.add_argument('--bin-width', default=0.25, type=float, help='Bin width in percentage points')
	parser.add_argument('--min-size', default=0, type=int, help='Minimum precinct size to include')
	parser.add_argument('--dpi', default=None, type=int, help='Resolution of the output image')
	parser.add_argument('-o', '--output', default='history.png', help='Output file')
	args = parser.parse_args()

	D = election_data.load(args.data)

	plt.figure(figsize=(12, 4))
	plot(D, title=os.path.basename(args.data), binwidth=args.bin_width, minsize=args.min_size)
	plt.savefig(args.output, bbox_inches='tight', dpi=args.dpi)
	plt.close()
