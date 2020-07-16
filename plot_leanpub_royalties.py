"""Generate a few plots for leanpub royalties.

Download a CSV of leanpub royalties, then use this script to generate various plots.

Get more help with:

    python plot_leanpub_royalties.py --help
"""

from collections import defaultdict
from itertools import chain

import click
import matplotlib.pyplot as plt
import pandas


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
def combined(filename):
    "Bar plot of combined books sales for day"
    df = pandas.read_csv(filename, parse_dates=['Date Purchased (UTC)'])
    g = df.groupby('Date Purchased (UTC)')
    data = ((date, len(sales)) for date, sales in g)
    data = list(zip(*data))

    plt.bar(*data)
    plt.show()


@cli.command()
@click.argument('filename', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
def per_book(filename):
    "Stacked bar plot showing daily sails of each book"

    # TODO: This should be an argument to the function (defaulting to this set)
    titles = ('The Python Apprentice', 'The Python Journeyman', 'The Python Master')

    df = pandas.read_csv(filename, parse_dates=['Date Purchased (UTC)'])
    g = df.groupby(['Date Purchased (UTC)', 'Book Title'])

    def sales_chart(book_title):
        "Dict of date->sales-count for a given title"
        data = defaultdict(lambda: 0)
        data.update(dict((date, len(sales))
                         for (date, title), sales in g
                         if title == book_title))
        return data

    sales_charts = [sales_chart(title) for title in titles]

    all_dates = sorted(set(chain(*sales_charts)))

    sales_counts = [[chart[date] for date in all_dates]
                    for chart in sales_charts]

    for index, chart in enumerate(sales_counts):
        plt.bar(all_dates, chart, label=titles[index],
                bottom=None if index == 0 else sales_counts[index - 1])

    plt.legend()
    plt.show()


if __name__ == '__main__':
    cli()
