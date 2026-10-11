# Scenario 16 --- Hangman Challenge

A multi-round terminal word-guessing game written in Python. The game
supports word categories, hints, difficulty levels, scoring, winning
streaks, and in-memory session statistics.

## Features

-   **Categories:** Choose from the categories provided in `words.py`
    (currently `technology`, `science`, and `culture`).
-   **Difficulty levels:** Each level changes the number of lives and
    the score multiplier.
-   **Guess validation:** A previously guessed correct or incorrect
    letter is rejected without changing the round state.
-   **Hints:** Request one available hint per round with `/hint`.
-   **Scoring:** Round score depends on the current winning streak and
    selected difficulty. Using a hint applies a difficulty-scaled
    penalty.
-   **Session statistics:** Tracks rounds played, rounds won, and the
    best winning streak for the current run.
-   **Input feedback:** Invalid input and unknown commands receive clear
    feedback without being treated as letter guesses.
-   **Terminal interface:** The project is designed to run in a
    command-line terminal; it does not include a graphical UI.

## Project structure

``` text
16_hangman/
├── main.py       # Application entry point
├── game.py       # Game flow, round state, guesses, hints, scoring and difficulty
├── words.py      # Word categories and hint data
├── stats.py      # In-memory session statistics
├── requirements.txt
└── README.md
```

## Requirements

-   Python 3
-   No additional packages are required beyond those declared in
    `requirements.txt`.

## Run the game

Open a terminal in the project directory and run:

``` bash
python main.py
```

Use the integrated terminal in your IDE so that interactive `input()`
prompts can receive keyboard input. If the program is run through an
output-only runner, it may appear to stop at a prompt because that panel
does not accept input.

## How to play

1.  Start the program with `python main.py`.
2.  Select a category shown by the game, or enter `q` to exit at the
    category prompt.
3.  Select a difficulty: `easy`, `medium`, or `hard`.
4.  Guess one alphabetic letter at a time.
5.  Enter `/hint` to request a hint when one is available.
6.  Enter `/quit` to leave the current round/session.
7.  After a round, choose whether to play another round.

Commands are case-insensitive after input is stripped and normalized.

## Difficulty and scoring

  Difficulty     Starting lives   Score multiplier
  ------------ ---------------- ------------------
  Easy                        8                 ×1
  Medium                      6                 ×2
  Hard                        4                 ×3

The round score on a win is calculated from the base score and the
updated winning streak:

``` text
base round score = (5 + current streak) × difficulty multiplier
```

If a hint was used, the penalty equals the selected difficulty
multiplier:

``` text
round score = max(0, base round score - hint penalty)
```

The score is added to the cumulative session score after a win. A lost
round awards zero points. The selected difficulty sets the starting
lives for each new round; round-specific state such as guessed letters,
wrong guesses, lives, and hint usage is reset at the start of a round.

## Session statistics

The `SessionStats` class in `stats.py` tracks:

-   **Rounds played:** Number of rounds recorded as completed.
-   **Rounds won:** Number of rounds won.
-   **Best streak:** Highest consecutive-win streak reached during the
    session.

The current streak increases after a win and resets after a loss. The
best streak remains unchanged when a loss resets the current streak.
Statistics are held in memory and reset when the program is restarted;
no file or database persistence is used.

## Task implementation summary

### Task 1 --- Guess-state correctness

The `guess()` method validates input and checks both the correct-guess
set and wrong-guess set before processing a letter:

``` python
if letter in self.guessed or letter in self.wrong:
    return "Already guessed."
```

This prevents repeated correct guesses from being processed again and
prevents repeated incorrect guesses from consuming additional lives. A
new incorrect letter is added to `self.wrong` and costs one life; a new
correct letter is added to `self.guessed`.

### Task 2 --- Complete the session model

`HangmanGame` creates one `SessionStats` instance for the whole session.
When a round ends, the game records whether it was won and the current
streak. Starting another round resets round-specific state without
resetting the cumulative score, current streak, or session statistics.

### Task 3 --- Difficulty and scoring

The `DIFFICULTIES` configuration defines lives and score multipliers for
Easy, Medium, and Hard. The selected difficulty is used to initialize
each round's lives and calculate its score. Hint penalties scale with
the difficulty multiplier.

### Task 4 --- Robust input and feedback

Input is routed explicitly:

-   A single alphabetic character is handled as a guess.
-   `/hint` requests a hint.
-   `/quit` exits the current game flow.
-   Unknown slash commands are rejected as unknown commands.
-   Empty, numeric, multi-letter, and special-character guesses are
    rejected by `guess()`.
-   Invalid category and difficulty selections are rejected before a
    round starts.
-   A hint that is unavailable should not consume the hint; a repeated
    hint should return one clear response.
-   Methods return feedback and the caller prints it once, avoiding
    duplicate messages.

## Testing checklist

Run the following manual tests in the terminal. Compare state
immediately before and after each action.

  -----------------------------------------------------------------------------
  Test              Input/action      Expected result        State that should
                                                             remain unchanged
  ----------------- ----------------- ---------------------- ------------------
  First correct     Enter a letter    `Correct.`             Lives, score,
  guess             present in the                           streak, and
                    word                                     session statistics
                                                             do not change
                                                             directly from the
                                                             guess

  Repeated correct  Enter the same    `Already guessed.`     Lives, score,
  guess             correct letter                           guessed set,
                    again                                    streak, and
                                                             statistics

  First wrong guess Enter a letter    `Wrong.`               Score, streak, and
                    absent from the                          session
                    word                                     statistics; lives
                                                             decreases by one

  Repeated wrong    Enter the same    `Already guessed.`     Lives, score,
  guess             wrong letter                             guessed set, wrong
                    again                                    set contents,
                                                             streak, and
                                                             statistics

  Empty input       Press Enter       `Enter one letter.`    All game and
                    without a value                          session state

  Number input      Enter `7`         `Enter one letter.`    All game and
                                                             session state

  Multiple letters  Enter `abc`       `Enter one letter.`    All game and
                                                             session state

  Special           Enter a symbol    `Enter one letter.`    All game and
  characters        such as `!`                              session state

  Invalid category  Enter a category  `Unknown category.`;   Round and session
                    not listed by the no round starts        state
                    game                                     

  Valid category    Enter a listed    Category is selected   Existing session
                    category          and flow continues     score and
                                                             statistics

  Hint              Enter `/hint`     Hint text appears once Lives and
                    when a hint is                           guessed-letter
                    available                                sets; hint use
                                                             affects the win
                                                             score

  Repeated hint     Enter `/hint`     A single "Hint already Hint state and
                    again in the same used" response         score beyond the
                    round                                    already-recorded
                                                             hint penalty

  Unavailable hint  Request a hint    "No hint available."   `hint_used`,
                    for a word                               score, lives, and
                    without hint data                        guessed letters

  Quit              Enter `/quit`     One quit message and   No guess, life
                    during a round    exit from the          loss, or win score
                                      round/session flow     should be applied
                                                             by the quit action

  Unknown command   Enter             `Unknown command.`     All game and
                    `/something`                             session state

  Difficulty: Easy  Start an Easy     8 starting lives; ×1   Cumulative session
                    round             multiplier             state

  Difficulty:       Start a Medium    6 starting lives; ×2   Cumulative session
  Medium            round             multiplier             state

  Difficulty: Hard  Start a Hard      4 starting lives; ×3   Cumulative session
                    round             multiplier             state

  Difficulty change Play Hard, then   Starting lives are 4,  Score and session
                    Easy, then Hard   8, then 4              statistics persist

  Multiple rounds   Win, win, lose,   Rounds played: 1, 2,   Best streak must
                    win               3, 4; rounds won: 1,   not be erased by a
                                      2, 2, 3; current       loss
                                      streak: 1, 2, 0, 1;    
                                      best streak: 1, 2, 2,  
                                      2                      

  Completed word    Guess every       Round ends as a win    No extra guess
                    distinct letter                          should be
                    in the secret                            processed after
                    word                                     the round has
                                                             ended
  -----------------------------------------------------------------------------

## Four-round statistics example

For the sequence **win → win → loss → win**, the expected session
statistics are:

  --------------------------------------------------------------------------
   After round Result          Rounds   Rounds won      Current  Best streak
                               played                    streak 
  ------------ --------- ------------ ------------ ------------ ------------
             1 Win                  1            1            1            1

             2 Win                  2            2            2            2

             3 Loss                 3            2            0            2

             4 Win                  4            3            1            2
  --------------------------------------------------------------------------

## Implementation notes

-   Keep the existing project structure and code modular.
-   Keep all game state in memory; do not add CSV, JSON, SQLite, or
    other persistence.
-   No GUI is included because this scenario is specified as a terminal
    game.
-   The conversation used to prepare these changes notes that the
    proposed code and test plan were not executed against the user's
    local files. Run the tests above against the current local version
    before claiming that all tests pass.
-   Make sure the local `game.py` contains the fixes from Tasks 1--4;
    the public repository version referenced in the conversation did not
    necessarily contain the latest local changes.

## Submission checklist

-   [ ] Record a 10-second video **before** changes showing the original
    repeated-wrong-guess bug.
-   [ ] Record a 10-second video **after** changes showing the fix and
    new features.
-   [ ] Test the boundary and invalid-input cases in this README.
-   [ ] Confirm no unnecessary dependencies or persistent storage were
    added.
-   [ ] Include the complete Chat/LLM conversation link with the
    submission.
