from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd

from matplotlib.figure import Figure

    # defining the graph
# def instagram_likes(instagram_scraped):
#     fig = plt.figure()
#     #x = instagram_scraped['Created_Time']
#     #y = instagram_scraped['Likes Count']
#     plt.hist(instagram_scraped['Likes Count'])
#     fig.suptitle('Distribution of Likes on Instagram Posts', fontsize=20)
#     plt.xlabel('Amount of Posts', fontsize=18)
#     plt.ylabel('Likes', fontsize=16)
#     fig_size = plt.rcParams["figure.figsize"]
#     #fig_size[0] = 40
#     #fig_size[1] = 20
#     #plt.rcParams["figure.figsize"] = fig_size
#     #note: figure size is currently restricted to some configuration in html/flash end



# Displays all the graphs 

def instagram_graph(instagram_scraped):

    fig = plt.figure(figsize=(8,6))

    ax1 = plt.subplot2grid((3,3), (0,0), colspan=3, rowspan=1)
    instagram_scraped['Comments Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Comments Count")


    ax2 = plt.subplot2grid((3,3), (1,0), colspan=3, rowspan=1)
    instagram_scraped['Likes Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Likes Count")


    ax3 = plt.subplot2grid((3,3), (2,0), colspan=3, rowspan=1)
    plt.hist(instagram_scraped['Likes Count'])
    plt.title('Distribution of Likes on Instagram Posts', fontsize=20)
    plt.xlabel('Amount of Posts', fontsize=18)
    plt.ylabel('Likes', fontsize=16)
    fig_size = plt.rcParams["figure.figsize"]

    fig.tight_layout()

