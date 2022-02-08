from contextlib import redirect_stdout
import rejection_criteria as rejection_criteria
from correction_structure import *

USERNAMES_PATH = "usernames.txt"

DEVOIRS_PATH = "devoirs/dev%d.txt"
CORRECTIONS_PATH = "corrections/dev%d_corr.txt"
SEPARATOR = "    "

# SOURCE HOMEWORK FILE STRUCTURE
HOMEWORK_SPLITTER = "------------------------"  # What separates homeworks in source, if in single file
HOMEWORK_ROOT_PATH = "/home/www-ens/"  # Path right before the username

# CLASS LIST INPUT COLUMN NAMES
NAME = "PRENOM"
LAST_NAME = "NOM"
STUDENT_NUMBER = "MATRICULE"
USERNAME = "LOGIN"
ID = "DGTIC"

# HOMEWORK COMMENTS
NO_COMMENT_TO_ADD = "Aucune retroaction à fournir"
DID_NOT_GIVE_IN_HOMEWORK = "Pas soumis de devoir"
DONE_IMPROPERLY = "Pas de code html dans le devoir/Permission denied/Pas suivi les consignes"


def write_file(file_path: str, file_contents: [str]):
    """
    Export contents
    :param file_path: file to write to
    :param file_contents: contents to write,
    :return:
    """
    with open(file_path, 'w') as f:
        with redirect_stdout(f):
            print(file_contents)


def main():
    usernames_unparsed = open(USERNAMES_PATH, "r", encoding="utf-8").read().splitlines()
    IFT1005 = Group(usernames_unparsed)

    dev0_excepts = []
    dev0_zeroes = []

    dev0 = Homework("index.html",
                    open(DEVOIRS_PATH % 0, "r", encoding="utf-8").read(),
                    dev0_zeroes,
                    rejection_criteria.tp0,
                    dev0_excepts)

    IFT1005.correct_with_output(dev0,
                                1,
                                True,
                                [])


if __name__ == '__main__':
    main()
