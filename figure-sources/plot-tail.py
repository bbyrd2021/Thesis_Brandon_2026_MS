"""Slide-friendly count view of the verified, nested log-z tail definitions."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
root = Path(__file__).resolve().parent
d = json.loads((root / 'train-counts.json').read_text())
rows = sorted(d['rows'], key=lambda r: -r['train_boxes'])
n = np.array([r['train_boxes'] for r in rows])
z = np.array([r['z'] for r in rows])
g = d['geometric_mean']
deep = 10 ** (d['mean_log10'] - 0.5 * d['std_log10_population'])
assert (z < 0).sum() == 47 and (z < -0.5).sum() == 28
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14})
fig, ax = plt.subplots(figsize=(12, 7))
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.14, top=0.84)
gray, coral, red = ('#004684', '#FEDC93', '#FDB927')
x = np.arange(1, 87)
ax.axvspan(39.5, 86.5, color=coral, alpha=0.1)
ax.axvspan(58.5, 86.5, color=red, alpha=0.09)
ax.bar(x, n, width=0.88, color=np.where(z < -0.5, red, np.where(z < 0, coral, gray)), zorder=3)
ax.set(yscale='log', xlim=(0.3, 86.7), ylim=(30, 2000000.0), xlabel='86 triplet classes, most to least frequent', ylabel='Training boxes (log scale)')
ax.set_xticks([])
ax.set_yticks([100, 1000, 10000, 100000, 1000000], ['100', '1k', '10k', '100k', '1M'])
ax.tick_params(axis='y', labelsize=12)
ax.grid(axis='y', alpha=0.14, zorder=0)
ax.spines[['top', 'right']].set_visible(False)
for y, c, label in [(g, coral, 'z = 0  ·  geometric mean ≈ 6,434'), (deep, red, f'z = −0.5  ·  ≈ {deep:,.0f} boxes')]:
    ax.axhline(y, color=c, linestyle='--', linewidth=1.4, zorder=4)
    ax.text(2, y * 0.77, label, color=gray, fontsize=12, weight='bold', va='top', bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 3}, zorder=5)
for start, y, label, c in [(39.5, 600000.0, 'Tail: 47 classes  ·  z < 0', coral), (58.5, 150000.0, 'Deeper tail: 28\nz < −0.5', red)]:
    ax.annotate('', xy=(start, y), xytext=(86.5, y), arrowprops={'arrowstyle': '|-|', 'color': c, 'lw': 1.6})
    ax.text((start + 86.5) / 2, y * 1.2, label, ha='center', va='bottom', fontsize=13, weight='bold', color=gray)
ax.annotate('Most common\n225,813 boxes', xy=(1, n.max()), xytext=(3, 500000.0), fontsize=13, weight='bold', color=gray, arrowprops={'arrowstyle': '->', 'color': gray, 'lw': 1.3})
for ext in ['png', 'svg', 'pdf']:
    fig.savefig(root / f'triplet-tail-counts-aggie.{ext}', dpi=220, facecolor='white')
print(f'Geometric mean: {g:.3f}; z=-0.5 count threshold: {deep:.3f}')