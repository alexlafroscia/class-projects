# Chat Server

##Goal:
To gain insight into using cryptography to secure client/server communications.

##High-level description:
You will be developing a secure chat server for this assignment.  Users will use a client application to connect to a running server. Once connected, users should be able to send messages to the server. Any messages sent to the server should be relayed to all users connected to the server.

You will secure the communications between each client and server. You can assume that the server is trusted by all users. We will simply be using cryptography to "protect" the messages en route from client to server and vice versa.

You are provided a good amount of code to work with. First, you are give the working **unsecure** old_code/ChatClient.java and old_code/ChatServer.java. These can server as a model for how the client and server applications should run and you can feel free to base your project on this code. You are further given a working **secure** SecureChatServer.java, and a set of RSA keys to be used by the server (keys.txt). In order to complete the project, you will need to write a secure client to interact with this secure server (which you should name "SecureChatClient.java"), and two symmetric ciphers ("Add128.java" and "Substitute.java") that implement the provided SymCipher.java interface.

## Additional Comments

More of a general comment on the project as a whole; there were very few details about the Substitute and Add128 classes that were discussed in the README.  A lot of assumptions had to be made, since there weren't any specifics about how those classes were to be implemented.  I hope that I made the right assumptions; everything does work correctly, though, so I hope that's all that matters.

Another note: I'm not sure if you're using a diffing program to check if we changed the Server file, but in case you are, I did change the file only to use spaced instead of tabs, since my Vim set up makes tabs hard to read.  Everything else is exactly the same, I just changed the whitespace.

