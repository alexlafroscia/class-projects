/**
 * CS/COE 1501
 * Primitive chat client.
 * This client connects to a server so that messages can be typed and forwarded
 * to all other clients.  Try it out in conjunction with ChatServer.java.
 * You will need to modify / update this program to incorporate the secure elements
 * as specified in the Assignment sheet.  Note that the PORT used below is not the
 * one required in the assignment -- be sure to change that and also be sure to
 * check on the location of the server program regularly (it may change).
 */
import java.util.*;
import java.io.*;
import java.net.*;
import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
import java.math.*;

@SuppressWarnings("serial")
public class SecureChatClient extends JFrame implements Runnable, ActionListener {

  public static final int PORT = 8765;

  ObjectInputStream myReader;
  ObjectOutputStream myWriter;
  JTextArea outputArea;
  JLabel prompt;
  JTextField inputField;
  String myName, serverName;
  Socket connection;
  SymCipher cipher;

  /**
   * Create a new chat client.
   * When a new client is created, make a new connection to the socket
   * connection running on the designated port, as well as the incoming and
   * outgoing connections to send a receive messages on.
   */
  public SecureChatClient () {
    try {

    myName = JOptionPane.showInputDialog(this, "Enter your user name: ");
    serverName = JOptionPane.showInputDialog(this, "Enter the server name: ");
    InetAddress addr = InetAddress.getByName(serverName);
    connection = new Socket(addr, PORT);   // Connect to server with new socket

    // Set up the stream reader and writer
    myWriter = new ObjectOutputStream(connection.getOutputStream());
    myWriter.flush();
    myReader = new ObjectInputStream(connection.getInputStream());

    // Get the public key (e) and mod value (n) from the server
    BigInteger serverPublicKey = (BigInteger)myReader.readObject();
    System.out.println("E value: " + serverPublicKey);
    BigInteger serverModValue = (BigInteger)myReader.readObject();
    System.out.println("N value: " + serverModValue);

    // Create the cipher object
    String cipherType = (String)myReader.readObject();
    if (cipherType.equals("Add")) {
      System.out.println("Cipher type: Add128");
      this.cipher = new Add128();
    } else if (cipherType.equals("Sub")) {
      System.out.println("Cipher type: Substitution");
      this.cipher = new Substitute();
    } else {
      System.out.println("An error occured during authentication; exitting");
      System.exit(1);
    }

    // Get the cipher key for the client
    BigInteger cipherKey = new BigInteger(1, this.cipher.getKey());
    System.out.println("Cipher key: " + cipherKey);

    // Send the encrypted version of the client's key to the server
    BigInteger encryptedClientKey = RSAHelper.encrypt(serverPublicKey, serverModValue, cipherKey);
    myWriter.writeObject(encryptedClientKey);
    myWriter.flush();

    // Write name to the server
    myWriter.writeObject(cipher.encode(myName));
    myWriter.flush();

    this.setTitle(myName);      // Set title to identify chatter

    Box b = Box.createHorizontalBox();  // Set up graphical environment for user
    outputArea = new JTextArea(8, 30);
    outputArea.setEditable(false);
    b.add(new JScrollPane(outputArea));

    outputArea.append("Welcome to the Chat Group, " + myName + "\n");

    inputField = new JTextField("");  // This is where user will type input
    inputField.addActionListener(this);

    prompt = new JLabel("Type your messages below:");
    Container c = getContentPane();

    c.add(b, BorderLayout.NORTH);
    c.add(prompt, BorderLayout.CENTER);
    c.add(inputField, BorderLayout.SOUTH);

    Thread outputThread = new Thread(this);  // Thread is to receive strings from server
    outputThread.start();

    addWindowListener(
      new WindowAdapter() {
        public void windowClosing(WindowEvent e) {
          try {
            myWriter.writeObject(cipher.encode("CLIENT CLOSING"));
            myWriter.flush();
          } catch (IOException error) {
            System.err.print(error);
          }
          System.exit(0);
         }
      }
    );

    setSize(500, 200);
    setVisible(true);

    } catch (Exception e) {
      e.printStackTrace();
      System.out.println("Problem starting client!");
    }
  }


  /**
   * When a new thread is made, try to get messages from the server and display
   * them in the chat log
   */
  public void run() {
    while (true) {
      try {
        byte[] encryptedMessage = (byte[])myReader.readObject();
        String currMsg = this.cipher.decode(encryptedMessage);
        outputArea.append(currMsg + "\n");
      } catch (Exception e) {
        System.out.println(e +  ", closing client!");
        break;
      }
    }
    System.exit(0);
  }


  /**
   * Send a message from the client to the server.
   * Gets the message from the chat interface when the user enters the text.
   * Encrypts the text and sends it to the server as a byte array
   *
   * @param e The action object, containing the text
   */
  public void actionPerformed(ActionEvent e) {
    String currMsg = e.getActionCommand();
    inputField.setText("");
    try {
      currMsg = myName + ": " + currMsg;
      myWriter.writeObject(this.cipher.encode(currMsg));
      myWriter.flush();
    } catch (IOException error) {
      error.printStackTrace();
    }
  }

  public static void main(String [] args) {
     SecureChatClient JR = new SecureChatClient();
     JR.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
  }
}

