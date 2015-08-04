import matplotlib.pyplot as plt

#     defining the graph
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
#     #note: figure size is currently restricted to mpl_config.py


# Displays all the graphs


def instagram_graph(instagram_scraped):

    fig = plt.figure(figsize=(8, 6))

    plt.subplot2grid((3, 3), (0, 0), colspan=3, rowspan=1)
    instagram_scraped['Comments Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Comment Count Per Post", fontsize=20)
    plt.ylabel('Total Comments')
    plt.xlabel('Most Recent to Least Recent')

    plt.subplot2grid((3, 3), (1, 0), colspan=3, rowspan=1)
    instagram_scraped['Likes Count'].plot(kind='bar', alpha=.55)
    plt.title("Total Like Count Per Post", fontsize=20)
    plt.xlabel('Most Recent to Least Recent')
    plt.ylabel('Total Likes')

    plt.subplot2grid((3, 3), (2, 0), colspan=3, rowspan=1)
    plt.hist(instagram_scraped['Likes Count'])
    plt.title('Test Graph (Please Ignore)', fontsize=20)
    plt.xlabel('Amount of Posts')
    plt.ylabel('Likes')
    plt.rcParams["figure.figsize"]

    fig.tight_layout()
