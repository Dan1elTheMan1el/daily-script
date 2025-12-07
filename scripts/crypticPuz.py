import puz
import requests
from urllib.parse import parse_qs
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
webhookURL = os.getenv("CROSSWORD_WEBHOOK")

month = datetime.datetime.now().month
day = datetime.datetime.now().day
year = datetime.datetime.now().year

puzData = requests.get(f"https://data.puzzlexperts.com/puzzleapp-v3/data.php?psid=100000160&date={year}-{month:02d}-{day:02d}").json()
puzJSON = {}
for key, value in parse_qs(puzData["cells"][0]["meta"]["data"]).items():
    if len(value) == 1:
        puzJSON[key] = value[0]
    else:
        puzJSON[key] = value

puzzle = puz.Puzzle()
puzzle.width = int(puzJSON["num_columns"])
puzzle.height = int(puzJSON["num_rows"])
puzzle.title = puzJSON["title"]

# Build solution
solution = ["." * puzzle.width for _ in range(puzzle.height)]
i = 0
while f"word{i}" in puzJSON:
    word = puzJSON[f"word{i}"]
    row = int(puzJSON[f"start_j{i}"])
    col = int(puzJSON[f"start_k{i}"])
    direction = puzJSON[f"dir{i}"]
    for j in range(len(word)):
        if direction == "a":
            solution[row] = solution[row][:col + j] + word[j] + solution[row][col + j + 1:]
        else:
            solution[row + j] = solution[row + j][:col] + word[j] + solution[row + j][col + 1:]
    i += 1

puzzle.solution = "".join(solution)

# Build fill
fill = ""
for r in range(puzzle.height):
    for c in range(puzzle.width):
        if solution[r][c] == ".":
            fill += "."
        else:
            fill += "-"
puzzle.fill = fill

# Sort words by starting cell
words = []
i = 0
while f"word{i}" in puzJSON:
    row = int(puzJSON[f"start_j{i}"])
    col = int(puzJSON[f"start_k{i}"])
    direction = puzJSON[f"dir{i}"]
    words.append((row, col, direction, i))
    i += 1
words.sort()

# Build clues
clues = []
for _, _, _, i in words:
    clues.append(puzJSON[f"clue{i}"])

puzzle.clues = clues
puzzle.save(f"data/puzArchive/crypticpuz_{year}_{month:02d}_{day:02d}.puz")

# Send puzzle to webhook
requests.post(webhookURL, files={"file": open(f"data/puzArchive/crypticpuz_{year}_{month:02d}_{day:02d}.puz", "rb")})