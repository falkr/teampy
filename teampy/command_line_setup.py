import teampy
from colorama import init

import click
from .core import Teampy
from . import __version__


@click.version_option(version=__version__)
def print_teampy():
    print(r" _                                   ")
    print(r"| |_ ___  __ _ _ __ ___  _ __  _   _ ")
    print(r"| __/ _ \/ _` | '_ ` _ \| '_ \| | | |")
    print(r"| ||  __/ (_| | | | | | | |_) | |_| |")
    print(r" \__\___|\__,_|_| |_| |_| .__/ \__, |")
    print(r"                        |_|    |___/ ")


@click.group()
@click.version_option(teampy.__version__)
def teampy():
    """
    Teampy is a collection of tools for team-based learning.
    """
    pass


def create_scratch_card_file():
    _ = (
        "# This file contains codes for scratch cards, so that you\n"
        "# do not have to read them in every time you use them.\n"
        "# Since we do not know the solutions on your scratch cards, you\n"
        "# have to edit this file on your own.\n"
        "#\n"
        "# All lines preceeded by a #, like these, are a comments.\n"
        "#\n"
        '# This is an example for an entry for a scratch card with name "F017":\n'
        "# F017: b c b a c d a c d c\n"
        "# Simply add your own cards in the lines below, but without any # in front.\n"
    )


@teampy.command()
@click.option("--example", is_flag=True, default=False, help="add example content")
def setup(example):
    """
    Create default setup for a course.

    This command creates the file skelettons for students, teams
    and scratch cards.

    If the --example option is specified, the command also populates the files
    with some content so you can play with the tool before creating your own
    course.
    """
    click.echo("Setup a new course.")


@teampy.command()
def sum():
    """
    Sum up the results of a course.
    """
    click.echo("Sum up a course.")
    teampy = Teampy()
    path = teampy.find_main_directory()
    print(path)

    # find all result files
    # for each result file, findout which RAT it belongs to

    def merge_in_rats(df, stmpy_path):
        for rat in [
            "rat1",
            "rat2",
            "rat3",
            "rat4",
            "rat5",
            "rat6",
            "rat7",
            "rat8",
            "rat9",
        ]:
            dfr = pd.read_excel("{}/{}/results.xlsx".format(stmpy_path, rat))
            dfr = dfr[["id", "score"]]
            dfr.rename(columns={"score": rat}, inplace=True)
            print(dfr.head())
            df = df.merge(dfr, on="id", how="left")
        for rat in ["rat3", "rat4", "rat5", "rat6", "rat7"]:
            dfr = pd.read_excel("{}/{}/results_2.xlsx".format(stmpy_path, rat))
            dfr = dfr[["id", "score"]]
            dfr.rename(columns={"score": rat}, inplace=True)
            print(dfr.head())
            df = df.merge(dfr, on="id", how="left")
        return df


if __name__ == "__main__":
    pass
