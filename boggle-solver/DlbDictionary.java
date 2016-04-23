/*
 * DlbDictionary.java
 * Author: Alex LaFroscia
 * Date: Jan 28, 2015
 */

public class DlbDictionary implements DictionaryInterface {

  private Node root;

  public DlbDictionary() {
    this.root = new Node('\0');
  }

  public boolean add(String s) {
    StringBuilder sb = new StringBuilder(s);
    sb.append('\0');
    boolean result = searchAndAdd(sb, this.root);
    return result;
  }

  private boolean searchAndAdd(StringBuilder sb, Node node) {
    boolean result = false;

    if (sb.length() == 0) {
      return true;
    }

    // Get the first character and remove it from the front of the `sb`
    char c = sb.charAt(0);
    sb = sb.deleteCharAt(0);

    Node nodeWithCharValue = node.findValueInChildren(c);
    if (nodeWithCharValue == null) {
      // If none of the children have the current `c` value
      Node newChild = node.addChild(c);
      result = searchAndAdd(sb, newChild);
    } else {
      result = searchAndAdd(sb, nodeWithCharValue);
    }

    return result;
  }

  public int search(StringBuilder sb) {
    StringBuilder sbcopy = new StringBuilder(sb);
    sbcopy.append('\0');

    int result = searchForString(sbcopy, this.root);
    return result;
  }

  private static int searchForString(StringBuilder sb, Node node) {
    char c = sb.charAt(0);
    sb = new StringBuilder(sb.substring(1));

    int result = 0;

    Node searchNode = node.findValueInChildren(c);
    if (sb.length() == 0) {

      // The length of the string is zero, so we're at the end of the string
      // If one of the children is the null terminator, then we know that we
      // have found a complete string.
      // If it has the terminator as a child AND some other child as well, then
      // we know that the search term is a complete string AND a prefix
      // If it does not have the null terminator as a child, but it does have
      // some number of children, then we know that it is _only_ a prefix
      // Also, if the length of the search string is 0, the last character to be
      // found must be the terminator value
      if (searchNode == null & node.numChildren() >= 1) {
        // Has some value that is not the terminator as a child
        result = 1;
      } else if (searchNode != null & node.numChildren() > 1) {
        // Has the terminator and some other value as children
        result = 3;
      } else if (searchNode != null & node.numChildren() == 1) {
        // Has only the terminator as a child
        result = 2;
      }
    } else if (searchNode == null) {
      // We know that we haven't checked every character in the string because
      // the SB's length is not 0
      // We also didn't find the next character in the search string, so we know
      // that the value isn't in the tree at all
      result = 0;
    } else {
      // Otherwise, we need to keep looking for the end of the string!
      result = searchForString(sb, searchNode);
    }

    return result;
  }

  private class Node {

    public char value;
    public Node sibling;
    public Node child;

    public Node(char value) {
      this.value = value;
    }

    public Node addSibling(char c) {
      Node f = this;
      while(f.sibling != null) {
        f = f.sibling;
      }
      f.sibling = new Node(c);
      return f.sibling;
    }

    public Node addChild(char c) {

      Node newNode;
      if (this.child == null) {
        // If the child is null, make the child a new node
        newNode = new Node(c);
        this.child = newNode;
      } else {
        // If the child isn't null, add a new sibling to that chain
        newNode = this.child.addSibling(c);
      }
      return newNode;
    }

    /*
     * Returns the node if found, else returns `null`
     */
    public Node findValueInChildren(char c) {
      // Search, starting with the first child node
      Node f = this.child;
      while (f != null) {
        // Had to check for this separately because I was getting a null pointer
        // exception if I put this check inside the while loop's statement
        if (f.value == c) {
          break;
        }
        f = f.sibling;
      }
      return f;
    }

    public int numChildren() {
      int sum = 0;
      Node node = this.child;
      while (node != null) {
        sum++;
        node = node.sibling;
      }
      return sum;
    }

    @Override
    public String toString() {
      StringBuilder sb = new StringBuilder("Value: -> " + this.value);
      sb.append(" : Children -> " + this.numChildren());
      if (this.sibling != null) {
        sb.append(" : Sibling -> Yes");
      }
      return sb.toString();
    }
  }
}

