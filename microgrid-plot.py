
# coding: utf-8

# In[22]:


import pandas as pd
import geopandas as gpd
import numpy as np
import math
import random
import os

from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import DBSCAN
from scipy.spatial import Delaunay

import time
import matplotlib.pyplot as plt
import networkx as nx
from networkx_viewer import Viewer

from haversine import haversine

import plotly
import plotly.plotly as py
from plotly.graph_objs import *
from plotly.offline import init_notebook_mode, plot_mpl
import snap


import holoviews as hv
from holoviews.operation.datashader import aggregate, shade, datashade, dynspread
from holoviews.operation import decimate

import datashader as ds
import datashader.transfer_functions as tf
from datashader.layout import random_layout, circular_layout, forceatlas2_layout
from datashader.bundling import connect_edges, hammer_bundle



# In[15]:


hv.extension('matplotlib')
hv.extension('bokeh')


# In[5]:


T = nx.read_gml('https://github.com/a-sharma06/microgrid_plot/blob/master/data/T.gml')


# In[12]:


adrs = pd.read_csv('adrs.csv')
location2 = pd.read_csv('https://github.com/a-sharma06/microgrid_plot/blob/master/data/location2.csv')


# In[6]:


# =============================================================================
# Converting edgeinfo into a format which can be printed through datashader
# =============================================================================

#Getting edges as a pandas dataframe
Tedges = nx.to_pandas_edgelist(T)
#Tedges.head()
Tedges.source = pd.to_numeric(Tedges.source)
Tedges.target = pd.to_numeric(Tedges.target)


# In[9]:


#Tedges.isnull().values.any()
Tnodes = adrs[['GEO_ID','LATITUDE','LONGITUDE']]
Tnodes.columns=['id', 'x', 'y']
Tnodes.set_index('id', inplace=True)
#Tnodes.head()
#location2.loc["GEOID","LATITUDE", "LONGITUDE"]]


# In[10]:


direct = connect_edges(Tnodes, Tedges[['source','target']])


# In[28]:


location2.COORDS2


# In[32]:


# =============================================================================
# Plotting with Holoview and Datashade
# =============================================================================

get_ipython().magic(u'output size=150')
points = hv.Points((location2.LATITUDE, location2.LONGITUDE),label="Buildings")
paths = hv.Path([direct])
datashade(points) + datashade(paths)

