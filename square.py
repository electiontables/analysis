#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec 

import election_data

# Settings used in our papers:
# * AOAS-2016:				 binwidth=0.1,	addNoise=False, weights='voters', minsize = 0
# * Significance-2016: binwidth=0.25, addNoise=True,	weights='ones',	 minsize = 0
# * Significance-2018: binwidth=0.1,	addNoise=True,	weights='ones',	 minsize = 0

def histogram(D, leader_names, *, binwidth, weights='voters', minsize=0, noise=False, seed=1):
	rnd = np.random.RandomState(seed)
	edges = np.arange(-binwidth/2, 100 + binwidth/2, binwidth)
	centers = np.arange(0, 100, binwidth)

	D = election_data.filter(D, ballots_valid_invalid_min=1, voters_registered_min=minsize, voters_voted_le_voters_registered=True, foreign=False)
	leader = election_data.find_leader_score(D, leader_names)

	wval, wlbl = {
		'voters': (D.voters_registered, 'voters registered'),
		'given':  (D.voters_voted, 'ballots given'),
		'leader': (leader, 'ballots for leader'),
		'ones':   (np.ones(D.voters_registered.shape), 'polling stations'),
	}.get(weights)
	noise1 = np.zeros(len(D)) if not noise else rnd.rand(len(D)) - .5
	noise2 = np.zeros(len(D)) if not noise else rnd.rand(len(D)) - .5
	h = np.histogram2d(100 * (D.voters_voted + noise1) / D.voters_registered,
	                   100 * (leader + noise2) / D.ballots_valid_invalid,
	                   bins=edges, weights=wval)[0]
	return wlbl, centers, h

def plot(D, leader_names, title, binwidth=0.25, aspect = 3, spacing = 0.5, **kwargs):
	wlbl, centers, h = histogram(D, leader_names, binwidth=binwidth, **kwargs)
	ht = np.sum(h, axis=1)
	hr = np.sum(h, axis=0)

	ylog = int(np.ceil(np.log10(min(np.max(ht), np.max(hr))))) - 1

	plt.suptitle(title, size=20, y=0.925, va='baseline')
	matplotlib.gridspec.GridSpec(4, 4)

	plt.subplot2grid((4, 4), (0, 0), colspan = 3)
	plt.plot(centers, ht / (10 ** ylog), linewidth=1)
	plt.xticks(np.arange(0, 101, 10))
	plt.ylim(bottom = 0)
	plt.xlim(0, 100)
	plt.xlabel('Turnout %')
	plt.tick_params(right=True, top=False, left=False, bottom=True, labelright=True, labeltop=False, labelleft=False, labelbottom=True)

	plt.subplot2grid((4, 4), (1, 0), colspan = 3, rowspan = 3)
	plt.imshow(h.T, vmin=0, vmax=np.quantile(h[h>0], 0.95), origin='lower', extent=[0,100,0,100], interpolation='none')
	plt.axis('off')

	plt.subplot2grid((4, 4), (1, 3), rowspan = 3)
	plt.plot(hr / (10 ** ylog), centers, linewidth=1)
	plt.xlim(left = 0)
	plt.ylim(0, 100)
	plt.yticks(np.arange(0, 101, 10))
	plt.ylabel('Leader’s result %')
	plt.tick_params(right=False, top=True, left=True, bottom=False, labelright=False, labeltop=True, labelleft=True, labelbottom=False)

	plt.subplot2grid((4, 4), (0, 3), frameon=False)
	plt.text(0.5, 0.5, f'$\\times 10^{{{ylog}}}$ {wlbl}\nin ${binwidth}\\,\\%$ bin', wrap=True, ha='center', va='center')
	plt.axis('off')

	plt.subplots_adjust(hspace = spacing, wspace = spacing)

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
	parser.add_argument('-o', '--output', default='square.png', help='Output file')
	args = parser.parse_args()

	D = election_data.load(args.data)

	plt.figure(figsize=(9, 9))
	plot(D, leader_names = election_data.RU_LEADER, title=os.path.basename(args.data), binwidth=args.bin_width, weights=args.weights, minsize=args.min_size, noise=args.noise)
	plt.savefig(args.output, bbox_inches='tight')
	plt.close()
