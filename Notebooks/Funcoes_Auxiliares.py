
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import  ListedColormap
import seaborn as sns
import sklearn
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
from matplotlib.ticker import PercentFormatter
import numpy as np


os.environ['OMP_NUM_THREADS'] = '1'

def plot_elbow_silhouette(x, random_state = 41, range_k =(2,11)):

    """Gera os gráficos para os métodos Elbow e Silhouette.

    Parameters
    ----------
    X : pandas.DataFrame
        Dataframe com os dados.
    random_state : int, opcional
        Valor para fixar o estado aleatório para reprodutibilidade, por padrão 42
    range_k : tuple, opcional
        Intervalo de valores de cluster, por padrão (2, 11)
    """


    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15,5), tight_layout=True)

    elbow = {}
    silhouette = []

    k_range = range(*range_k)

    for i in k_range:
        kmeans = KMeans(n_clusters=i, random_state=random_state, n_init=10)
        kmeans.fit(x)
        elbow[i] = kmeans.inertia_

        labels = kmeans.labels_
        silhouette.append(silhouette_score(x, labels))

    sns.lineplot(x=list(elbow.keys()), y=list(elbow.values()), ax=axs[0])
    axs[0].set_xlabel('K')
    axs[0].set_xlabel('Inertia')
    axs[0].set_xlabel('Elbolw Method')

    sns.lineplot(x=list(k_range), y=silhouette, ax=axs[1])
    axs[1].set_xlabel('K')
    axs[1].set_xlabel('Silhouette Score')
    axs[1].set_xlabel('Silhouette Method')





def plot_clusters_2D(dataframe, columns, n_colors, centroids, show_centroids = True, show_points=False, column_custers = None):

    """Gerar gráfico 2D com os clusters.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    columns : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    n_colors : int
        Número de cores para o gráfico.
    centroids : np.ndarray
        Array com os centroides.
    show_centroids : bool, opcional
        Se o gráfico irá mostrar os centroides ou não, por padrão True
    show_points : bool, opcional
        Se o gráfico irá mostrar os pontos ou não, por padrão False
    column_custers : List[int], opcional
        Coluna com os números dos clusters para colorir os pontos
        (caso mostrar_pontos seja True), por padrão None
    """



    fig = plt.figure()

    ax = fig.add_subplot(111)

    cores = plt.cm.tab10.colors[:n_colors]
    cores = ListedColormap(cores)


    x = dataframe[columns[0]]
    y = dataframe[columns[1]]

    ligar_centreids = show_centroids
    ligar_pontos = show_points 

    for i, centroids in enumerate(centroids):

        if ligar_centreids:

            ax.scatter(*centroids, s=200,alpha=0.5)
            ax.text(*centroids, f"{i}", fontsize=10, horizontalalignment='center', verticalalignment='center')

        if ligar_pontos:

            s = ax.scatter(x,y, c=column_custers, cmap=cores)

            ax.legend(*s.legend_elements(), bbox_to_anchor=(1.4,1))

    ax.set_xlabel(columns[0])
    ax.set_ylabel(columns[1])
    ax.set_title('Clusters')

    plt.show()






def inspect_outliers(dataframe, colum, whisker_width=1.5):

    """Função para inspecionar outliers.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    column : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    whisker_width : float, opcional
        Valor considerado para detecção de outliers, por padrão 1.5

    Returns
    -------
    pd.DataFrame
        Dataframe com os outliers.
    """

    q1 = dataframe[colum].quantile(0.25)
    q3 = dataframe[colum].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - whisker_width * iqr
    upper_bound = q3 + whisker_width * iqr

    return dataframe[
        (dataframe[colum]<lower_bound) | (dataframe[colum]>upper_bound)
    ]



def pairplot(
    dataframe, columns, hue_column=None, alpha=0.5, corner=True, palette="tab10"
):
    """Função para gerar pairplot.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    columns : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    hue_column : str, opcional
        Coluna utilizada para hue, por padrão None
    alpha : float, opcional
        Valor de alfa para transparência, por padrão 0.5
    corner : bool, opcional
        Se o pairplot terá apenas a diagonal inferior ou será completo, por padrão True
    palette : str, opcional
        Paleta a ser utilizada, por padrão "tab10"
    """

    analysis = columns.copy() + [hue_column]

    sns.pairplot(
        dataframe[analysis],
        diag_kind="kde",
        hue=hue_column,
        plot_kws=dict(alpha=alpha),
        corner=corner,
        palette=palette,
    )



def plot_columns_percent_by_cluster(
    dataframe,
    columns,
    rows_cols=(2, 3),
    figsize=(15, 8),
    column_cluster="cluster",
):
    """Função para gerar gráficos de barras com a porcentagem de cada valor por cluster.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    columns : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    rows_cols : tuple, opcional
        Tupla com o número de linhas e colunas do grid de eixos, por padrão (2, 3)
    figsize : tuple, opcional
        Tupla com a largura e a altura da figura, por padrão (15, 8)
    column_cluster : str, opcional
        Nome da coluna com os números dos clusters, por padrão "cluster"
    """  

    fig, axs = plt.subplots(nrows=rows_cols[0], ncols=rows_cols[1], figsize=figsize, sharey=True)

    if not isinstance(axs, np.ndarray):
        axs = np.array(axs)


    for ax, col in zip(axs.flatten(), columns):
        h = sns.histplot(x=column_cluster, hue=col, data=dataframe, ax=ax, multiple='fill', stat='percent', discrete=True, shrink=0.8)

        n_clusters = dataframe[column_cluster].nunique()
        h.set_xticks(range(n_clusters))
        h.yaxis.set_major_formatter(PercentFormatter(1))
        h.set_ylabel('')
        h.tick_params(axis='both', which ='both', length=0)

        for bars in h.containers:
            h.bar_label(bars, label_type='center', labels=[f'{b.get_height():.1%}' for b in bars], color='white', weight='bold', fontsize=11)

        for bar in h.patches:
            bar.set_linewidth(0)

    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    plt.show()



def plot_columns_percent_hue_cluster(
    dataframe,
    columns,
    rows_cols=(2, 3),
    figsize=(15, 8),
    column_cluster="cluster",
    palette="tab10",
):
    """Função para gerar gráficos de barras com a porcentagem de cada valor com cluster
    como hue.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Dataframe com os dados.
    columns : List[str]
        Lista com o nome das colunas (strings) a serem utilizadas.
    rows_cols : tuple, opcional
        Tupla com o número de linhas e colunas do grid de eixos, por padrão (2, 3)
    figsize : tuple, opcional
        Tupla com a largura e a altura da figura, por padrão (15, 8)
    column_cluster : str, opcional
        Nome da coluna com os números dos clusters, por padrão "cluster"
    palette : str, opcional
        Paleta a ser utilizada, por padrão "tab10"
    """
    fig, axs = plt.subplots(
        nrows=rows_cols[0], ncols=rows_cols[1], figsize=figsize, sharey=True
    )

    if not isinstance(axs, np.ndarray):
        axs = np.array(axs)

    for ax, col in zip(axs.flatten(), columns):
        h = sns.histplot(
            x=col,
            hue=column_cluster,
            data=dataframe,
            ax=ax,
            multiple="fill",
            stat="percent",
            discrete=True,
            shrink=0.8,
            palette=palette,
        )

        if dataframe[col].dtype != "object":
            h.set_xticks(range(dataframe[col].nunique()))

        h.yaxis.set_major_formatter(PercentFormatter(1))
        h.set_ylabel("")
        h.tick_params(axis="both", which="both", length=0)

        for bars in h.containers:
            h.bar_label(
                bars,
                label_type="center",
                labels=[f"{b.get_height():.1%}" for b in bars],
                color="white",
                weight="bold",
                fontsize=11,
            )

        for bar in h.patches:
            bar.set_linewidth(0)

        legend = h.get_legend()
        legend.remove()

    labels = [text.get_text() for text in legend.get_texts()]

    fig.legend(
        handles=legend.legend_handles,
        labels=labels,
        loc="upper center",
        ncols=dataframe[column_cluster].nunique(),
        title="Clusters",
    )

    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    plt.show()
