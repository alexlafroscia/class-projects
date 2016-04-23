/*
 * Board.java
 * Author: Alex LaFroscia
 * Date: Jan 28, 2015
 */

import java.util.*;

public class Board {

  private static final int NUM_ROWS = 4;
  private static final int NUM_COLS = 4;

  private BoardSpace[][]      board;
  private String              name;
  public  DictionaryInterface foundWords;
  private DictionaryInterface dictionary;
  private Set<String>         foundWordsList = new HashSet<String>();

  public Board(String fileName, String dbType, char[] characterArray) {
    // Get name of board
    fileName = fileName.substring(5, 6);
    name = "Board " + fileName;

    // Set up dictionary
    if (dbType.equals("simple")) {
      foundWords = new SimpleDictionary();
    } else if (dbType.equals("dlb")) {
      foundWords = new DlbDictionary();
    }

    // Set up board
    board = new BoardSpace[NUM_ROWS][NUM_COLS];
    int k = 0;
    for (int i = 0; i < NUM_ROWS; i++) {
      for (int j = 0; j < NUM_COLS; j++) {
        board[i][j] = new BoardSpace(characterArray[k++]);
      }
    }
  }


  /**
   * Scans the board for words found in the given dictionary
   *
   * @param dictionary An instance of a DictionaryInterface that represents all
   *                   of the possible valid words
   */
  public Thread scan(DictionaryInterface dictionary) {
    this.dictionary = dictionary;
    Thread t = new Thread(new DictionarySearch(dictionary));
    t.start();
    return t;
  }


  /**
   * Start a new thread to search the board against the dictionary.
   *
   * This is a process that can take a long time, and I noticed that the way the
   * game is set up, we have a chance to do some keyboard IO during the same
   * time to get the guesses from the user of the program.  Instead of having an
   * awkward pause here, we can parallelize it and have the board searched while
   * the user guesses
   */
  private class DictionarySearch implements Runnable {

    private DictionaryInterface dictionary;

    public DictionarySearch(DictionaryInterface dictionary) {
      this.dictionary = dictionary;
    }

    /**
     * Kick off the search of the board.
     *
     * To make this a separate thread, we needed a new class with a run() method
     */
    public void run() {
      StringBuilder sb = new StringBuilder();

      // Run a search tree starting at each of the board's squares
      for (int i = 0; i < NUM_ROWS; i++) {
        for (int j = 0; j < NUM_COLS; j++) {
          search(i, j, sb);
        }
      }
    }

    /**
     * Check if a square is part of a string.
     *
     * Searches one square of the board for the given StringBuilder, then possibly
     * goes on to search further squares.
     *
     * Note: This is a recursive call
     *
     * @param x  The x value of the coordinates of the board square to check
     * @param y  The y value of the coordinates of the board square to check
     * @param sb The string builder that represents the current String being built
     *           and checked against the master dictionary.
     */
    private void search(int x, int y, StringBuilder sb) {
      BoardSpace square = board[x][y];

      // If the square has been used in this word already, skip it here
      if (square.checked) {
        return;
      } else {
        square.checked = true;
      }

      char c = square.value;
      c = Character.toLowerCase(c); // Normalize everything to lower case

      if (c == '*') {
        int ALPHABET_LENGTH = 26;
        char[] alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                           'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                           'w', 'x', 'y', 'z'};
        for (int i = 0; i < ALPHABET_LENGTH; i++) {
          StringBuilder sbNew = new StringBuilder(sb);
          sbNew.append(alphabet[i]);
          searchForString(x, y, square, sbNew);
        }
      } else {
        sb.append(c);
        searchForString(x, y, square, sb);
      }
    }

    private void searchForString(int x, int y, BoardSpace square, StringBuilder sb) {
      // Note: This could be refactored into less lines of code by making
      // extensive use of fallthrough, but in reality it makes the code a lot
      // harder to read.  Like they always say, write code for humans!
      switch(this.dictionary.search(sb)) {
        case 0:
          // sb not in dictionary, remove new character and return
          sb.deleteCharAt(sb.length() - 1);
          square.checked = false;
          return;
        case 1:
          // sb is a prefix; break to search
          break;
        case 2:
          // sb is in the dictionary but is _not_ a prefix.  Add it to the
          // dictionary, shorten sb and return
          foundWords.add(sb.toString());
          foundWordsList.add(sb.toString());
          sb.deleteCharAt(sb.length() - 1);
          square.checked = false;
          return;
        case 3:
          // sb is both in the dictionary _and_ is a prefix.  Add it to the
          // dictionary and break to search
          foundWords.add(sb.toString());
          foundWordsList.add(sb.toString());
          break;
        default:
          // If by some strange miracle you end up with a return value from
          // dictionary.search that isn't one of those values, just shorten sb and
          // return
          sb.deleteCharAt(sb.length() - 1);
          square.checked = false;
          return;
      }

      // Format the if statements to that the `x` and `y` statements line up
      //  Check X Value          Check Y Value        Search that square

      // North West
      if ((x - 1) >= 0        & (y - 1) >= 0      ) { search(x - 1, y - 1, sb); }
      // North
      if (                      (y - 1) >= 0      ) { search(x    , y - 1, sb); }
      // North East
      if ((x + 1) < NUM_ROWS  & (y - 1) >= 0      ) { search(x + 1, y - 1, sb); }
      // West
      if ((x - 1) >= 0                            ) { search(x - 1, y    , sb); }
      // East
      if ((x + 1) < NUM_ROWS                      ) { search(x + 1, y    , sb); }
      // South West
      if ((x - 1) >= 0        & (y + 1) < NUM_COLS) { search(x - 1, y + 1, sb); }
      // South
      if (                      (y + 1) < NUM_COLS) { search(x    , y + 1, sb); }
      // South East
      if ((x + 1) < NUM_ROWS  & (y + 1) < NUM_COLS) { search(x + 1, y + 1, sb); }

      // After checking each neighboring square, remove the last character from
      // sb, mark this square as not yet checked, and return
      sb.deleteCharAt(sb.length() - 1);
      square.checked = false;
      return;
    }

  }


  /**
   * Prints the dictionary of words found on this board.
   *
   * Takes the HashSet of words that were found on the board, converts it into
   * an ArrayList, sorts it, and prints it out.
   *
   */
  public void printDictionary() {
    ArrayList<String> sortedList = new ArrayList<String>(this.foundWordsList);
    Collections.sort(sortedList);
    for(String word: sortedList) {
      System.out.println(word);
    }
  }


  public int getDictionaryCount() {
    return foundWordsList.size();
  }


  @Override public String toString() {
    StringBuilder result = new StringBuilder();
    result.append(name + '\n');
    for (int i = 0; i < NUM_ROWS; i++) {
      StringBuilder row = new StringBuilder();
      for (int j = 0; j < NUM_COLS; j++) {
        row.append(board[i][j].value + " ");
      }
      row.append('\n');
      result.append(row);
    }
    return result.toString();
  }

  /*
   * BoardSpace
   * Author: Alex LaFroscia
   * Date: Jan 28, 2015
   *
   * Represents a single space on a Boggle board
   */
  private class BoardSpace {
    public boolean checked = false;
    public char value;

    public BoardSpace(char boardValue) {
      value = boardValue;
    }

  }

}

