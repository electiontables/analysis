#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import election_data

def plot(D, title, hours_begin = 8.00, hours_end = 20.00, linewidth = 0.02):
	time = [hours_begin] + [float(n.replace('turnout_', '').replace('h', '.')) for n in D.dtype.names if 'turnout_' in n] + [hours_end]
	turnout = np.vstack([D[n] for n in D.dtype.names if 'turnout_' in n] + [D.turnout]).T
	turnout = np.hstack([np.zeros_like(turnout[:, :1]), turnout])
	plt.suptitle(title)
	for subplot, diff, xlabel, ylabel  in [(211, False, '', 'Turnout %'), (212, True, 'Time', 'Turnout increase %')]:
		plt.subplot(subplot)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.gca().add_collection(matplotlib.collections.LineCollection(np.dstack([np.broadcast_to(time, turnout.shape), (np.hstack([turnout[:, :1], np.diff(turnout)]) if diff else turnout) * 100]), linewidth = linewidth))
		plt.xlim([hours_begin - 1, hours_end + 1])
		plt.ylim([0, 100 + 5])
		plt.vlines(time[1:],*plt.ylim(), linewidth=.5, color='black')
		plt.xticks(time, map('{:.0f}:00'.format, time))

if __name__ == '__main__':
	import os
	import argparse
	import matplotlib
	matplotlib.use('Agg')

	parser = argparse.ArgumentParser()
	parser.add_argument('data', nargs='?', metavar='DATA', default='https://github.com/schitaytesami/lab/releases/download/data-v2/2018.tsv.gz', help='Data file to use')
	parser.add_argument('--dpi', default=None, type=int, help='Resolution of the output image')
	parser.add_argument('-o', '--output', default='historytraj', help='Output directory')
	args = parser.parse_args()

	os.makedirs(args.output, exist_ok=True)

	D = election_data.load(args.data)
	R = election_data.regions(D)

	for region_code in R:
		print(region_code)
		plt.figure(figsize=(12, 8))
		plot(election_data.filter(D, region_code=region_code), title=R[region_code])
		plt.savefig(os.path.join(args.output, region_code + '.png'),
		            bbox_inches='tight', dpi=args.dpi)
		plt.close()
