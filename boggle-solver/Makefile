JAVAC=javac
sources = $(wildcard *.java)
classes = $(sources:.java=.class)

all: $(classes)

clean :
		rm -f *.class

%.class : %.java
		$(JAVAC) $<

test :
		java MyBoggle -d simple -b board1.txt

