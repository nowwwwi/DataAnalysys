import matplotlib.pyplot as plt


def make_scatter(df, title: str, x_axis: str, x_axis_name: str, y_axis: str, y_axis_name: str):
    x, y = df[x_axis], df[y_axis]

    plt.scatter(x, y, s=3)

    plt.title(title)
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)

    plt.savefig('figures/scatter.png')

    corr = df.corr()
    corr.to_csv('data/corr.csv')
