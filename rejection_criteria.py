from main import DONE_IMPROPERLY


def tp0(work: [str]) -> (bool, str):
    """
    Corrects the submitted homework. Here one can write a method to check certain lines
    of the homework and check for coherence/presence of certain things

    :param work: the work to correct
    :return: a tuple containing
        - a bool about whether the student should get a ZERO
        - a str comment if anything to add
    """
    a = False
    b = False
    comment = ""
    # check if student did everything correctly in hwk 1

    for line in work:
        if "<html>" in line:
            a = True
        if "</html>" in line:
            b = True

    # if missing something, give comment that indicates so
    if not (a or b):
        comment = DONE_IMPROPERLY

    # return pass/fail indicator and comment, if any
    return not (a or b), comment
