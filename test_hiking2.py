"""Acceptance tests for the Hiking2 exercise (Part 2 of the puzzle).

Each test runs your program as a whole, exactly as a user would: it writes
a map in a file, gives the name of this file on the command line, then
checks what your program prints and tries to explain what is wrong.

Run the tests from the exercise folder with:

    python test_hiking2.py
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

EXERCISE_DIR = Path(__file__).resolve().parent
SCRIPT = "hiking2.py"
USAGE = "Usage: python hiking2.py filename"
TIMEOUT = 10  # seconds
TIMEOUT_MESSAGE = ("Your program did not stop within {} seconds (infinite "
                   "loop?). Along a hiking trail, the height increases by "
                   "exactly 1 at each step: if your program can also go "
                   "down, it can go back and forth forever.".format(TIMEOUT))

# Each test case: (what is checked, rows of the map written in the file).
# The expected answer is computed by the answer() function below.
CASES = [
    ("map 01 (5 rows x 5 columns)", [
        "67518",
        "58911",
        "43480",
        "12363",
        "04101",
    ]),
    ("map 02 (8 rows x 5 columns)", [
        "45790",
        "91449",
        "12113",
        "35901",
        "59873",
        "03763",
        "55680",
        "74321",
    ]),
    ("map 04 (8 rows x 8 columns)", [
        "01296199",
        "12984110",
        "83779140",
        "74568730",
        "65431412",
        "21221010",
        "32787213",
        "45694677",
    ]),
    ("map 05 (12 rows x 12 columns)", [
        "265432012841",
        "679501983654",
        "789410198753",
        "858324987612",
        "985735902527",
        "114889603439",
        "279927112376",
        "768719796456",
        "933652008217",
        "435340839858",
        "848432638279",
        "997821048121",
    ]),
    ("map 06 (5 rows x 10 columns)", [
        "2631994467",
        "2015017789",
        "4324125692",
        "5898734156",
        "6753512347",
    ]),
    ("map 07 (10 rows x 10 columns)", [
        "7986749438",
        "5515824946",
        "7894977222",
        "6543083671",
        "6602172733",
        "7111055866",
        "6590603227",
        "7784098668",
        "8669194336",
        "6543265210",
    ]),
    ("map 08 (20 rows x 20 columns)", [
        "19411469087624410523",
        "58953659195545719989",
        "69437411045832922890",
        "16355321882581052432",
        "43333404444320299653",
        "53199577862653524053",
        "61358374553129327543",
        "85398775481764910672",
        "32855097955786996701",
        "98316182212154984151",
        "61547236303073375372",
        "33854327674587824372",
        "69965408473683963764",
        "43878342998780126167",
        "98550968539229038454",
        "65155333076178648963",
        "97726919886307654872",
        "80032098780230438901",
        "26344145626783022298",
        "05950032101021014192",
    ]),
    ("map 09 (20 rows x 40 columns)", [
        "9831182273654345526720204210664345282361",
        "3767139694013766875833736390630999026520",
        "1456927351172215514112376481017129358103",
        "0371553386354309917803985519928319943286",
        "1268351604933478132134594321910182756779",
        "1640875591542560496081603980318885611890",
        "8024799591468315970974789657765969830984",
        "3546196247858482347817651514623986765474",
        "2008959600993801456941129771102354245501",
        "6602902213497823941084285255933143137432",
        "8947073623533257778148630710312101240689",
        "7018220554678839571568197208012339506978",
        "6325404267782813944346099358658478684468",
        "5490449788992801802022834484306567893351",
        "4321096545401662278789121405217496048948",
        "7632187432372855826171102406789692114630",
        "8543418121893795600382341753598413456121",
        "9877676986754552098724357615487456907219",
        "6959480345866590152654169802256133898335",
        "7823141289879929454793278541855432165473",
    ]),
    ("map 11 (42 rows x 42 columns)", [
        "769410167676343210987612101012152190123875",
        "648565078985350349898925132101057280541998",
        "765612109854741256789721293540348781210987",
        "174543498767410109899812112478787670309876",
        "010893567896585010998927676707870101410963",
        "321989878983476523543932785434161452321054",
        "832452965371289430989765676501092965410123",
        "236771433410194321078956769830187874321010",
        "217365536761435012347855878798216989210107",
        "358676247572343201256398912981645010101016",
        "566567656232411510105289801293634321014527",
        "876898540170121491010708214604143410153454",
        "210787856083210780007612123783232300129623",
        "143298432378343661438781214230101010178010",
        "032156743207252123325668705371010128767123",
        "651089832376744715430799016410101230823232",
        "567398783469878506525786824501010341234541",
        "323985894278785434634347785632301250789650",
        "334856485547676343765254345503298765898701",
        "219898320118545654364567643014769896967810",
        "156781235007654823605894570125678987876923",
        "217648040432743764012144545034389878965434",
        "656549101232657656543230176945498569678925",
        "232323212323844567698961089876987654589876",
        "485212343232435458787432126967898983890945",
        "376507650107590189896501083458989892101233",
        "635898701012521018987872342329078701010112",
        "776789894307632567898943401210145670321021",
        "665856987654741540189834890101236543423232",
        "749764876745987651221985751032108216584378",
        "898985545556578946726654672127679921554447",
        "765394404327677867655443785658787862465787",
        "654562713276588945664914872566698779565659",
        "783117621103497664567897861410632873456789",
        "567021750212566989658988634324783976565478",
        "656722248701255698749010342223856894478398",
        "545485839812666549832106523238088785698988",
        "665176988701767276921013454349109698487630",
        "954987234317652327010104545673014525378343",
        "835478123654341218901767654782323432109254",
        "744767854367636963212676351123434321030341",
        "623896565252125872123260567659565010101650",
    ]),
    ("a map with a single row", [
        "0123456789",
    ]),
    ("a map with a single column", [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]),
    ("a 9 reached by 126 different trails counts 126 times", [
        "012345",
        "123456",
        "234567",
        "345678",
        "456789",
    ]),
    ("a trail does not go from one side of the map to the other", [
        "0987654321",
    ]),
]

# Map files given with the exercise: (what is checked, file name).
FILE_CASES = [
    ("file small_map.txt", "small_map.txt"),
    ("file large_map.txt", "large_map.txt"),
]

# Invalid command lines: (what is checked, arguments).
# The program must print the usage message and stop.
USAGE_CASES = [
    ("no file name", []),
    ("two file names", ["small_map.txt", "large_map.txt"]),
]

# A map written in a file without a newline at the end.
NO_FINAL_NEWLINE_CASE = ("a file without a newline at the end", [
    "0123",
    "7654",
    "8900",
])

# Frequent mistakes: (parameters of answer() reproducing the mistake,
# explanation). After all the tests, the explanations of the mistakes
# that give exactly the results printed by the program are shown.
MISTAKES = [
    ({"count": "summits"},
     "Your program seems to count the different 9s that each trailhead "
     "can reach (that is Part 1 of the puzzle!). In Part 2, the rating of "
     "a trailhead is the number of different hiking trails starting from "
     "it: a 9 reached by 3 trails counts 3 times. If your program "
     "remembers the positions already visited (in a set, for example), "
     "it never follows a second trail to the same 9."),
    ({"count": "trailheads"},
     "Your program seems to count the trailheads that can reach at least "
     "one 9. The answer is the sum of the ratings of all the trailheads."),
    ({"count": "union"},
     "Your program seems to count the 9s that can be reached from at "
     "least one trailhead. The answer is the number of different hiking "
     "trails, and each trailhead has its own trails: do not share the "
     "positions already visited between trailheads."),
    ({"diagonals": True},
     "Your program seems to move diagonally too: a hiking trail only "
     "goes up, down, left or right."),
    ({"step": "abs1"},
     "Your program seems to go down too: along a hiking trail, the "
     "height increases by exactly 1 at each step (0, 1, 2, ..., 9)."),
    ({"step": "increase"},
     "Your program seems to accept any increase of height: along a "
     "hiking trail, the height increases by exactly 1 at each step "
     "(from 3 you can go to 4, not to 5)."),
    ({"bounds": "wrap"},
     "Your program seems to go from one side of the map to the other: in "
     "Python, heights[-1] is not an error, it is the LAST row (and "
     "row[-1] the last column). Before using heights[row][col], check "
     "that 0 <= row < number of rows and 0 <= col < number of columns."),
    ({"bounds": "skip_last"},
     "Your program seems to never start from a 0 of the last row or of "
     "the last column: range(n) already stops at n - 1, so "
     "range(len(heights)) goes through all the rows."),
]

# Text typed if the program asks something (it should not).
UNEXPECTED_INPUT = ""


# ---------------------------------------------------------------------------
# Expected results
# ---------------------------------------------------------------------------

STEPS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAGONAL_STEPS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def neighbours(rows, row, col, diagonals=False, bounds="right"):
    """Return the positions next to (row, col) inside the map.

    The optional parameters reproduce frequent mistakes (see answer()).
    """
    nb_rows = len(rows)
    nb_cols = len(rows[0])
    steps = STEPS + DIAGONAL_STEPS if diagonals else STEPS
    positions = []
    for d_row, d_col in steps:
        new_row = row + d_row
        new_col = col + d_col
        if bounds == "wrap":
            # Only the upper bounds are checked: rows[-1] is the last row,
            # but (-1, col) is not the same position as (nb_rows - 1, col)
            # for the program. (Below -nb_rows, the program would crash.)
            if (-nb_rows <= new_row < nb_rows
                    and -nb_cols <= new_col < nb_cols):
                positions.append((new_row, new_col))
        elif 0 <= new_row < nb_rows and 0 <= new_col < nb_cols:
            positions.append((new_row, new_col))
    return positions


def is_step(height, next_height, step="+1"):
    """Return True if a trail may go from height to next_height.

    step: "+1" (right), "abs1" (+1 or -1) or "increase" (any increase).
    """
    if step == "+1":
        return next_height == height + 1
    if step == "abs1":
        return abs(next_height - height) == 1
    return next_height > height


def reachable_nines(rows, start, diagonals=False, step="+1",
                    bounds="right"):
    """Return the set of positions of the 9s reachable from start."""
    seen = {start}
    to_visit = [start]
    nines = set()
    while to_visit:
        row, col = to_visit.pop()
        height = int(rows[row][col])
        if height == 9:
            nines.add((row, col))
        for new_row, new_col in neighbours(rows, row, col, diagonals,
                                           bounds):
            next_height = int(rows[new_row][new_col])
            if ((new_row, new_col) not in seen
                    and is_step(height, next_height, step)):
                seen.add((new_row, new_col))
                to_visit.append((new_row, new_col))
    return nines


def nb_trails(rows, start, diagonals, step, bounds, known):
    """Return the number of different trails from start to a 9.

    known: dict of the numbers already computed, by position.
    """
    if start not in known:
        row, col = start
        height = int(rows[row][col])
        total = 1 if height == 9 else 0
        if height < 9:
            for position in neighbours(rows, row, col, diagonals, bounds):
                new_row, new_col = position
                if is_step(height, int(rows[new_row][new_col]), step):
                    total += nb_trails(rows, position, diagonals, step,
                                       bounds, known)
        known[start] = total
    return known[start]


def trailheads(rows, bounds="right"):
    """Return the positions of the 0s, row by row.

    If bounds is "skip_last", the last row and the last column are
    forgotten, as with range(len(rows) - 1).
    """
    nb_rows = len(rows)
    nb_cols = len(rows[0])
    if bounds == "skip_last":
        nb_rows -= 1
        nb_cols -= 1
    positions = []
    for row in range(nb_rows):
        for col in range(nb_cols):
            if rows[row][col] == "0":
                positions.append((row, col))
    return positions


def answer(rows, count="trails", diagonals=False, step="+1",
           bounds="right"):
    """Return the number the program should print for the map.

    The optional parameters reproduce frequent mistakes:
    - count: "trails" (right: number of different trails from the
      trailheads to the 9s), "summits" (sum of the numbers of 9s
      reachable from each trailhead, Part 1), "trailheads" (number of
      trailheads reaching a 9) or "union" (number of 9s reachable from
      at least one trailhead);
    - diagonals: if True, a trail may also move diagonally;
    - step: "+1" (right), "abs1" or "increase" (see is_step());
    - bounds: "right", "wrap" (only the upper bounds are checked, so
      negative indices go to the other side of the map) or "skip_last"
      (no trailhead in the last row and the last column).
    Return None if the mistake cannot give a result (infinite loop).
    """
    starts = trailheads(rows, bounds)
    if count == "trails":
        if step == "abs1":
            return None  # going up and down: infinitely many trails
        known = {}
        return sum(nb_trails(rows, start, diagonals, step, bounds, known)
                   for start in starts)
    all_nines = [reachable_nines(rows, start, diagonals, step, bounds)
                 for start in starts]
    if count == "trailheads":
        return sum(1 for nines in all_nines if nines)
    if count == "union":
        return len(set().union(*all_nines))
    return sum(len(nines) for nines in all_nines)  # "summits"


# ---------------------------------------------------------------------------
# Running the student's program
# ---------------------------------------------------------------------------

def run_program(arguments):
    """Run the program with the arguments.

    Return (stdout, stderr, return code), or None if the program
    did not stop in time.
    """
    try:
        # sys.executable is the Python running the tests,
        # so "python" vs "python3" does not matter.
        result = subprocess.run(
            [sys.executable, SCRIPT] + arguments,
            input=UNEXPECTED_INPUT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=EXERCISE_DIR,
            env=dict(os.environ, PYTHONIOENCODING="utf-8"),
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None
    stdout = result.stdout.replace("\r\n", "\n")
    stderr = result.stderr.replace("\r\n", "\n").strip()
    return stdout, stderr, result.returncode


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def show(text, max_lines=6, max_length=70):
    """Indent the lines of a text, with each line between quotes.

    Only the first lines are shown, and long lines are cut.
    """
    lines = text.splitlines()
    if not lines:
        return "    (nothing)"
    shown_lines = []
    for line in lines[:max_lines]:
        if len(line) > max_length:
            shown_lines.append(f"    {line[:max_length]!r}... (cut)")
        else:
            shown_lines.append(f"    {line!r}")
    if len(lines) > max_lines:
        shown_lines.append(f"    ... ({len(lines) - max_lines} more lines)")
    return "\n".join(shown_lines)


def last_lines(text, nb_lines=4):
    """Return the last lines of a text, indented."""
    lines = text.split("\n")[-nb_lines:]
    return "\n".join("    " + line for line in lines)


def plural(number, word):
    """Return e.g. '1 trailhead' or '3 trailheads'."""
    return f"{number} {word}" if number == 1 else f"{number} {word}s"


def show_map(rows, max_rows=10):
    """Return the map, indented, if it is small enough."""
    if len(rows) > max_rows:
        return None
    return "\n".join("    " + row for row in rows)


def explain_expected(rows, max_listed=6):
    """Explain how the expected answer is computed for the map."""
    starts = trailheads(rows)
    if not starts:
        return "The map has no trailhead (no 0), so the answer is 0."
    ratings = []
    known = {}
    for row, col in starts:
        rating = nb_trails(rows, (row, col), False, "+1", "right", known)
        if rating > 0:
            ratings.append(f"row {row} column {col} (rating {rating})")
    message = f"The map has {plural(len(starts), 'trailhead')} (0s)"
    if not ratings:
        return message + ", but none of them reaches a 9: the answer is 0."
    message += (f", {len(ratings)} of them can reach a 9 (rows and columns "
                f"are numbered from 0):\n    "
                + ", ".join(ratings[:max_listed]))
    if len(ratings) > max_listed:
        message += f"... ({len(ratings) - max_listed} more)"
    return message + f"\nSum of the ratings: {answer(rows)}."


def explain_crash(stderr):
    """Explain the most common errors that make the program crash."""
    message = f"Your program crashed:\n{last_lines(stderr)}"
    if "EOFError" in stderr:
        message += ("\nYour program asks the user something with input(). "
                    "It should not: the file name is given on the command "
                    "line, in sys.argv[1].")
    elif "IndexError" in stderr and "argv" in stderr:
        message += ("\nThere is no file name on the command line, so "
                    "sys.argv[1] does not exist. Before using it, check "
                    "len(sys.argv): if it is not 2, print the usage "
                    "message and stop.")
    elif "IndexError" in stderr:
        message += ("\nYour program looked outside the map (or outside a "
                    "row). Before using heights[row][col], check that "
                    "0 <= row < number of rows and 0 <= col < number of "
                    "columns.")
    elif "FileNotFoundError" in stderr:
        message += ("\nYour program tried to open a file that does not "
                    "exist: open the file whose name is in sys.argv[1].")
    elif "ValueError" in stderr and "int()" in stderr:
        message += ("\nint() was given something that is not a digit. "
                    "Maybe the '\\n' at the end of each line, or an empty "
                    "line: str.split() and str.splitlines() give the lines "
                    "without their '\\n'.")
    elif "TypeError" in stderr and "str" in stderr and "int" in stderr:
        message += ("\nYour program mixes str and int: the characters of "
                    "the file are str ('7'), convert them with int() "
                    "before computing with them.")
    elif "RecursionError" in stderr:
        message += ("\nYour function calls itself again and again: does "
                    "it go back down? Along a trail, the height increases "
                    "by exactly 1 at each step, so a trail has 10 positions "
                    "at most.")
    return message


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_usage(arguments):
    """Check that an invalid command line prints the usage message only.

    Return None if the test passes, else an error message.
    """
    result = run_program(arguments)
    if result is None:
        return TIMEOUT_MESSAGE
    stdout, stderr, _ = result
    if stdout == USAGE + "\n" and stderr == "":
        return None
    # sys.exit("Usage: ...") writes the message on stderr: it is accepted too.
    if stdout == "" and stderr == USAGE:
        return None

    lines = stdout.splitlines()
    printed = "Your program printed:\n" + show(stdout)
    if "Traceback" in stderr and USAGE in stdout:
        return (f"Your program printed the usage message, but then it went "
                f"on and crashed. It should stop right after the usage "
                f"message (e.g. with sys.exit()).\n{printed}\n"
                f"{explain_crash(stderr)}")
    if "Traceback" in stderr:
        return explain_crash(stderr)
    if any(line.strip() == USAGE for line in lines):
        if len(lines) > 1:
            return (f"Your program printed the usage message, but then it "
                    f"went on. It should stop right after the usage message "
                    f"(e.g. with sys.exit()).\n{printed}")
        return (f"Your program should print only {USAGE!r}, nothing else "
                f"(not even spaces).\n{printed}")
    if any(line.strip().lower() == USAGE.lower() for line in lines):
        return (f"Check the case and the spelling: the message must be "
                f"exactly {USAGE!r}.\n{printed}")
    if any(line.startswith("Usage") for line in lines):
        return f"The usage message must be exactly {USAGE!r}.\n{printed}"
    if any(line.strip().isdigit() for line in lines):
        return (f"There must be exactly one file name on the command line: "
                f"your program should print {USAGE!r}.\n{printed}")
    return f"Your program should print {USAGE!r}.\n{printed}"


def check_number(stdout):
    """Check that the program printed a single number.

    Return (error message or None, number printed or None if not valid).
    """
    lines = stdout.splitlines()
    printed = "Your program printed:\n" + show(stdout)
    if not lines:
        return "Your program printed nothing.", None
    if len(lines) > 1:
        message = ("Your program should print a single line (the answer). "
                   "Remove your extra print() (map, ratings, debugging...).")
        return f"{message}\n{printed}", None

    line = lines[0]
    if line.isdigit():
        return None, int(line)
    if line.startswith(USAGE):
        return (f"Your program printed the usage message, but the command "
                f"line is valid.\n{printed}"), None
    if line.strip().isdigit():
        return (f"Nothing should be printed before or after the number "
                f"(not even spaces).\n{printed}"), None
    if line.endswith(".0") and line[:-2].isdigit():
        return (f"The answer must be an integer (int), not a float: "
                f"print 36, not 36.0.\n{printed}"), None
    if any(char.isdigit() for char in line):
        return (f"Your program should print only the number, without any "
                f"text.\n{printed}"), None
    return f"Your program should print a number.\n{printed}", None


def check_map(path, rows):
    """Run one test on the file `path` containing the map `rows`.

    Return (error message or None if the test passes,
            number printed by the program or None if not valid).
    """
    result = run_program([str(path)])
    if result is None:
        return TIMEOUT_MESSAGE, None
    stdout, stderr, _ = result
    if "Traceback" in stderr:
        return explain_crash(stderr), None
    message, given = check_number(stdout)
    if message is not None:
        return message, None

    expected = answer(rows)
    if given != expected:
        return (f"Your program printed {given} instead of {expected}.\n"
                + explain_expected(rows)), given
    return None, given


def diagnose(observations):
    """Explain the wrong results, using all the results of the program.

    observations: list of (map, number printed by the program).
    Return the explanations of the frequent mistakes (alone, or else two
    at a time) that give exactly the same results as the program.
    """
    def consistent(parameters):
        for rows, given in observations:
            if answer(rows, **parameters) != given:
                return False
        return True

    causes = []
    for parameters, explanation in MISTAKES:
        if consistent(parameters):
            causes.append(explanation)
    if causes:
        return causes
    for i, (parameters_1, explanation_1) in enumerate(MISTAKES):
        for parameters_2, explanation_2 in MISTAKES[i + 1:]:
            if parameters_1.keys() & parameters_2.keys():
                continue  # the two mistakes are about the same thing
            if consistent(parameters_1 | parameters_2):
                causes.append(explanation_1 + "\n    AND " + explanation_2)
    return causes


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def main():
    sys.stdout.reconfigure(errors="replace")
    use_colors = sys.stdout.isatty() and (
        os.name != "nt" or "WT_SESSION" in os.environ)
    green = "\033[32m" if use_colors else ""
    red = "\033[31m" if use_colors else ""
    reset = "\033[0m" if use_colors else ""

    if not (EXERCISE_DIR / SCRIPT).is_file():
        print(f"No {SCRIPT} found in {EXERCISE_DIR}")
        return 1

    nb_ok = 0
    nb_tests = len(CASES) + len(FILE_CASES) + 1 + len(USAGE_CASES)
    observations = []  # (map, number printed by the program)
    nb_wrong_results = 0

    shown = []  # explanations already printed

    def report(description, message, details):
        """Print the result of one test.

        An explanation already printed for a previous test is not
        repeated (nor the details of the test): only what the program
        printed is shown.
        """
        if message is None:
            print(f"{green}✔{reset} {description}")
            return 1
        print(f"{red}✗{reset} {description}")
        explanation, separator, printed = message.partition(
            "\nYour program printed:")
        if explanation in shown:
            message = "Same problem as above." + separator + printed
        else:
            shown.append(explanation)
            for detail in details:
                print("    " + detail.replace("\n", "\n    "))
        print("    " + message.replace("\n", "\n    ") + "\n")
        return 0

    with tempfile.TemporaryDirectory() as tmp_dir:
        tests = []
        all_cases = CASES + [NO_FINAL_NEWLINE_CASE]
        for number, (description, rows) in enumerate(all_cases, start=1):
            path = Path(tmp_dir) / f"map_{number:02}.txt"
            text = "\n".join(rows)
            if (description, rows) != NO_FINAL_NEWLINE_CASE:
                text += "\n"
            path.write_text(text, encoding="utf-8")
            details = []
            small_map = show_map(rows)
            if small_map is None:
                details.append(f"A map of {len(rows)} rows and "
                               f"{len(rows[0])} columns: to try it "
                               f"yourself, copy it from {Path(__file__).name}"
                               f" into a file.")
            else:
                details.append("Map in the file:\n" + small_map)
            tests.append((description, path, rows, details))
        for description, file_name in FILE_CASES:
            path = EXERCISE_DIR / file_name
            if not path.is_file():
                print(f"{red}✗{reset} {description}")
                print(f"    {file_name} not found in {EXERCISE_DIR}\n")
                continue
            rows = path.read_text(encoding="utf-8").split()
            tests.append((description, file_name, rows,
                          [f"Command: python {SCRIPT} {file_name}"]))

        stopped = False
        for description, path, rows, details in tests:
            message, given = check_map(path, rows)
            if given is not None:
                observations.append((rows, given))
                if message is not None:
                    nb_wrong_results += 1
            nb_ok += report(description, message, details)
            if message == TIMEOUT_MESSAGE:
                print("The other tests are not run: fix this problem "
                      "first.\n")
                stopped = True
                break

    if not stopped:
        for description, arguments in USAGE_CASES:
            message = check_usage(arguments)
            command = " ".join(["python", SCRIPT] + arguments)
            nb_ok += report(f"usage message: {description}", message,
                            [f"Command: {command}"])

    if nb_wrong_results > 0:
        causes = diagnose(observations)
        if not causes:
            print("To find your mistake, take a small map that fails, "
                  "print the rating of each trailhead and compare these "
                  "ratings with the expected ones (and remove these print() "
                  "afterwards).\n")
        else:
            title = "Probable cause" if len(causes) == 1 else "Possible causes"
            print(f"{title} of the wrong results, considering all the tests:")
            for cause in causes:
                print("  - " + cause)
            print()

    color = green if nb_ok == nb_tests else red
    print(f"Validated: {color}{nb_ok}/{nb_tests}{reset}")
    return 0 if nb_ok == nb_tests else 1


if __name__ == "__main__":
    sys.exit(main())
