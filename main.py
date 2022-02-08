from correction_structure import *

"""
Main file structure:

main.py -> where config is done for class list, homework paths, correction output paths
        -> where one can indicate certain configs for the homework, ie: should
        there be any exceptions to the correction criteria?
        
correction_structure.py -> logic regarding correction + output generation 

rejection_criteria.py -> contains methods to help correct individual homeworks,
        which are then passed as parameter to overall program 

"""

USERNAMES_PATH = "usernames.txt"

DEVOIRS_PATH = "devoirs/dev%d.txt"
CORRECTIONS_PATH = "correction/dev%d_corr.txt"
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


def main():
    # class list input here
    usernames_unparsed = open(USERNAMES_PATH, "r", encoding="utf-8").read().splitlines()
    # create group
    IFT1005 = Group(usernames_unparsed)

    # HOMEWORK INPUT + CORRECTION
    dev0_excepts = []
    dev0_zeroes = []

    dev0 = Homework("index.html",
                    open(DEVOIRS_PATH % 0, "r", encoding="utf-8").read(),
                    tp0,
                    dev0_zeroes,
                    dev0_excepts)

    IFT1005.correct_with_output(dev0,
                                1,
                                True)


if __name__ == '__main__':
    main()
