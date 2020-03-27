#!/bin/bash
set -x

sudo yum -y install java-1.8.0-openjdk-devel
java -version
javac -version

cat > HelloWorld.java <<HELLO
public class HelloWorld {
  public static void main(String[] args) {
    System.out.println("Hello World!");
  }
}
HELLO

javac HelloWorld.java && java HelloWorld

rm -f HelloWorld*