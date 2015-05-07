import pandas as pd
import matplotlib as mpl
import brewer2mpl
import mpld3

pd.options.display.mpl_style = 'default'
bmap = brewer2mpl.get_map('Set1','qualitative',8,reverse=False)
colors = bmap.mpl_colors
smallfont = {'family' : 'Open Sans',
'weight' : 'normal',
'size'   : 8}

font = {'family' : 'Open Sans',
'weight' : 'normal',
'size'   : 12}

bigfont = {'family' : 'Open Sans',
'weight' : 'normal',
'size'   : 18,}

mpl.rc('font', **font)
mpl.rc('lines', linewidth=1)
mpl.rcParams['legend.fontsize'] = 10