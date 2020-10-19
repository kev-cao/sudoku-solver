# sudoku-solver
Sudoku solver implemented with Python.

## Context
Built for an assignment in my Introduction to AI course - we were tasked to implement a sudoku solver using a backtracking algorithm. A contest was held after the assignment to find the best algorithm. There were two rounds, and after round 1, students were permitted to improve on their algorithm before the championship round in round 2. My implementation was able to win first place in both rounds.

## How to Run
You can view the test cases in the `/tests` folder. Each sudoku board is stored in a spreadsheet as a `.csv` file. The solved boards are stored in the `/solutions` folder.

The winning implementation is in `a2.py`. `round1.py` contains the code from the first round. To run the winning implementation, simply run the command `python contest_benchmark.py` to test it against all of the test cases. If you wish to run the implementation against a certain board, change the file path at the bottom of `a2.py` to match the board you wish to test it against.

## Round 1 Results
![Round 1 Results](https://i.imgur.com/EGXVPHm.jpg)

## Round 2 Results
![Round 2 Results](https://i.imgur.com/jGQ1t5s.jpg)

## Final Results
![Final Results](https://i.imgur.com/5RNUfcq.jpg)
