from main import HOMEWORK_SPLITTER, \
    HOMEWORK_ROOT_PATH, \
    SEPARATOR, \
    NAME, \
    LAST_NAME, \
    USERNAME, \
    STUDENT_NUMBER, \
    ID, \
    DID_NOT_GIVE_IN_HOMEWORK, \
    CORRECTIONS_PATH, \
    write_file, \
    NO_COMMENT_TO_ADD


# "COURS:CODE-PERM:PROG  :NOM :PRENOM:CRED:NAT:NOTE:DEB:SECT:LOGIN:DGTIC:MATRICULE:"
class Homework:
    def __init__(self, name: str,
                 text: str,
                 rejection_criteria,
                 automatic_zero: [str],
                 exceptions_not_zero=None):
        """

        :param name: name of homework file
        :param text: unparsed text file
        :param rejection_criteria: method to reject or accept a homework from a student
        (see rejection_criteria.py for examples)
        :param automatic_zero: list of students that automatically get a zero here
        :param exceptions_not_zero: list of students that shouldn't be given a zero
        """
        self.name = name
        self.text = text
        self.automatic_zero = automatic_zero
        self.exceptions_not_zero = exceptions_not_zero
        self.rejection_criteria = rejection_criteria
        self.hwk = {}
        self.blacklist = []

    def set_blacklist(self, blacklist):
        """
        Words to reject a homework, example homeworks that weren't filtered out
        :param blacklist:
        :return:
        """
        self.blacklist = blacklist

    def parse_hwk(self):
        """
        Note: it's important to adapt this to different
        homework file structures
        """
        divided = self.text.split(HOMEWORK_SPLITTER)
        divided = list(filter(lambda x: x != "\n", divided))
        for assignment in divided:
            lines = assignment.split("\n")
            lines = list(filter(lambda x: x != "", lines))
            if any([x in assignment for x in self.blacklist]):
                continue
            username = ""
            path = ""
            work = []
            for idx, line in enumerate(lines):
                if idx == 0:
                    splitted = line
                    splitted = splitted.replace(HOMEWORK_ROOT_PATH, "")
                    splitted = splitted.split("/")
                    username = splitted[0]
                    for elem in splitted[1:]:
                        path += elem + "/"
                else:
                    work.append(line)
            self.hwk[username] = {"path": path, "work": work}

    def correct(self, blacklist=None):
        if blacklist:
            self.set_blacklist(blacklist)

        self.parse_hwk()

        for student in self.hwk:
            rejection, comment = self.rejection_criteria(self.hwk[student]["work"])
            if (rejection and (student not in self.exceptions_not_zero)) or student in self.automatic_zero:
                self.hwk[student]["grade"] = 0
            else:
                self.hwk[student]["grade"] = 100
            if comment and (student not in self.exceptions_not_zero):
                self.hwk[student]["comment"] = comment
            else:
                self.hwk[student]["comment"] = None

    def get_zeroes(self):
        for student in self.hwk:
            if self.hwk[student]["grade"] == 0:
                print(student, self.hwk[student]["work"])

    def __str__(self):
        return str(self.text)


class Group:
    class Student:
        def __init__(self, first_name, last_name, username, matricule, userid):
            self.first_name = first_name
            self.last_name = last_name
            self.username = username
            self.matricule = matricule
            self.userid = userid
            self.grades_minidevs = []
            self.comments_minidevs = []

        def __str__(self):
            return self.first_name + SEPARATOR \
                   + self.last_name + SEPARATOR \
                   + self.username + SEPARATOR \
                   + self.matricule

        def add_grade(self, grade):
            self.grades_minidevs.append(grade)

        def _ge__(self, other):
            return self.last_name >= other.last_name

    def __init__(self, usernames_unparsed):
        self.usernames = list(
            filter(lambda username: (username is not None), [[elem.strip() for elem in line.split(":")] for line in
                                                             usernames_unparsed]))
        self.headers = {header: header_idx for header_idx, header in enumerate(self.usernames[0])}
        self.usernames = self.usernames[1:]
        self.students = {student_info[self.headers[USERNAME]]: self.Student(student_info[self.headers[NAME]],
                                                                            student_info[self.headers[LAST_NAME]],
                                                                            student_info[self.headers[USERNAME]],
                                                                            student_info[self.headers[STUDENT_NUMBER]],
                                                                            student_info[self.headers[ID]])
                         for student_info in self.usernames}

    def __str__(self):
        # Gets group list
        result = ""
        for key in [NAME, LAST_NAME, USERNAME, STUDENT_NUMBER]:
            result += key + SEPARATOR
        result += "\n"
        for student in self.students:
            result += str(student) + "\n"
        return result

    def get(self, header_name):
        return [user[self.headers[header_name.upper()]] for user in self.usernames] \
            if header_name.upper() in self.headers.keys() else []

    def find(self, username: str, alert_if_not_in_class=False) -> Student:
        """
        Find a Student in the class by username
        :param username: the username to find
        :param alert_if_not_in_class: if True, will print to console the users in the
        homework which are not in the class list.
        :return: a Student object
        """
        if username in self.students:
            return self.students[username]
        else:
            if alert_if_not_in_class:
                print("Did not find username ", username, "in class")

    def assign_grades(self, homework: Homework, homework_number: int):
        """
        Assign grades from homework to students in class
        :param homework: source homework
        :param homework_number:
        """
        for author in homework.hwk:
            student = self.find(author)
            if student:
                student.grades_minidevs.insert(homework_number - 1, homework.hwk[author]["grade"])
                student.comments_minidevs.append(homework.hwk[author]["comment"])

        for student in self.students:
            # in case the student did not give in their homework
            if len(self.students[student].grades_minidevs) < homework_number:
                self.students[student].grades_minidevs.insert(homework_number - 1, 0)
            if len(self.students[student].comments_minidevs) < homework_number:
                self.students[student].comments_minidevs.insert(homework_number - 1,
                                                                DID_NOT_GIVE_IN_HOMEWORK)

    def correct(self, homework: Homework, homework_number: int, blacklist=None):
        """
        Corrects a given homework and assigns its grades to respective students in group
        :param homework: homework to correct
        :param homework_number:
        :param blacklist: [str] a list of strings that help blacklist homeworks that might not have
        been filtered out
        """
        homework.correct(blacklist)
        self.assign_grades(homework, homework_number)

    def correct_with_output(self, homework: Homework, homework_number: int,
                            write_to_file: bool, blacklist=None):
        """
        Corrects a given homework and assigns its grades to respective students in group,
        and then output this to either a file or in the console.
        :param homework: homework to correct
        :param homework_number:
        :param write_to_file: whether to output to file or in console
        :param blacklist:
        :return:
        """
        self.correct(homework, homework_number, blacklist)
        if write_to_file:
            write_file(CORRECTIONS_PATH % homework_number, self.get_group_results(
                homework_number))
        else:
            print(self.get_group_results(
                homework_number))

    def get_students_with_specific_grade(self, grade: int, homework_number: int) -> str:
        """
        Get a list of the students with a specific grade for a specific homework
        :param grade: the grade we want to match, from 0 to 100
        :param homework_number:
        :return: a string with all the students of this grade
        """
        final_file_txt = ""
        for student in self.students:
            if len(self.students[student].grades_minidevs) >= homework_number \
                    and self.students[student].grades_minidevs[homework_number - 1] == grade:
                final_file_txt += str(self.students[student]) + "\n"
        return final_file_txt

    def get_group_results(self, homework_number: int) -> str:
        """
        Produce a list of all the class' results for a specific homework number
        :param homework_number: the homework to get the results for
        :return: the list of results
        """
        final_file_txt = "USERNAME" + "\t" + "NOTE" + "\t" + "COMMENT" + "\n"
        for student in self.students:
            # USERNAME
            final_file_txt += str(self.students[student].userid) + "\t"

            # FULL NAME
            # final_file_txt += self.students[student].first_name + \
            #                   " " + self.students[student].last_name + "\t"
            #

            if len(self.students[student].grades_minidevs) < homework_number:
                final_file_txt += str(0) + "\t"

            else:
                final_file_txt += str(self.students[student].grades_minidevs[homework_number - 1]) + "\t"

            if self.students[student].comments_minidevs[homework_number - 1] is not None:
                final_file_txt += str(self.students[student].comments_minidevs[homework_number - 1])
            else:
                final_file_txt += NO_COMMENT_TO_ADD

            final_file_txt += "\n"
        return final_file_txt
