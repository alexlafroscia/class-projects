/*
 * MyBoggle.java
 * Author: Alex LaFroscia
 * Date: Jan 28, 2015
 */

import java.io.FileReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.text.DecimalFormat;
import java.util.*;

public class MyBoggle {
  public static void main(String[] args)
    throws IOException, InterruptedException {

    int i = 0;
    String arg, boardName = null, dbType = null;

    // Parse arguments, setting `boardName` to the specified name of the board
    // and `dbType` to the type of database to use for the dictionary
    while (i < args.length && args[i].startsWith("-")) {
      arg = args[i++];
      if (arg.equals("-b")) {
        boardName = args[i++];
      } else if (arg.equals("-d")) {
        dbType = args[i++];
      }
    }

    // If the board name hasn't been set, quit the game
    if (boardName == null) {
      System.out.println("Error: Board name is required to play Boggle!");
      System.exit(1);
    }

    // If the db type hasn't been set, quit the game
    if (dbType == null) {
      dbType = "simple";
    }


    // Make Dictionary
    DictionaryInterface dictionary = null;
    if (dbType.equals("simple")) {
      dictionary = new SimpleDictionary();
    } else if (dbType.equals("dlb")) {
      dictionary = new DlbDictionary();
    } else {
      System.out.println("Error: Unsupported dictionary type");
      System.exit(1);
    }


    // Make Boggle Board
    BufferedReader br = new BufferedReader(new FileReader(boardName));
    StringBuilder sb = new StringBuilder();
    String line = br.readLine();

    try {
      while (line != null) {
        sb.append(line);
        line = br.readLine();
      }
    } catch(IOException error) {
      System.out.println("There was a problem reading the board file\n");
      System.exit(1);
    } finally {
      br.close();
    }

    System.out.println("\nYour Boggle board for: " + boardName + "\n");

    Board board = new Board(boardName, dbType, sb.toString().toCharArray());
    System.out.println(board);

    // Read in dictionary from file
    br = new BufferedReader(new FileReader("dictionary.txt"));
    line = br.readLine();

    try {
      while (line != null) {
        dictionary.add(line);
        line = br.readLine();
      }
    } catch(IOException error) {
      System.out.println("There was a problem reading the dictionary file\n");
      System.exit(1);
    } finally {
      br.close();
    }

    // Search the board for words in the dictionary that was just created
    Thread t = board.scan(dictionary);

    System.out.println("What words can you find on the board?");
    System.out.println("Press <return> after each found word.");
    System.out.println("Pressing <return> on an empty line signals that " +
                       "you're finished guessing\n");

    Scanner s = new Scanner(System.in);
    String input = null;
    ArrayList<String> inputStrings = new ArrayList<String>();

    while (!(input = s.nextLine()).equals("")) {
      inputStrings.add(input);
    }

    t.join();

    System.out.println("There are " + board.getDictionaryCount() + " total words:");
    board.printDictionary();

    ArrayList<String> validWords = new ArrayList<String>();
    for (String word: inputStrings) {
      int result = board.foundWords.search(new StringBuilder(word));
      if (result == 2 || result == 3) {
        validWords.add(word);
      }
    }

    float foundPercentage = (float)validWords.size() / (float)board.getDictionaryCount();
    foundPercentage = foundPercentage * 100;
    DecimalFormat df = new DecimalFormat();
    df.setMaximumFractionDigits(2);

    System.out.printf("\nYou found %d of them (%.2f%%)\n", validWords.size(), foundPercentage);
    for(String word: validWords) {
      System.out.println(word);
    }

    System.out.println("\nThanks for playing Boggle!");
  }
}

