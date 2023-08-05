# Installing FCSS yourself

## Python Implementation
```sh
git clone https://github.com/PixelatedLagg/fcss/
cd fcss/Grammar

## Compile grammar
java -jar ../Jars/antlr-4.13.0-complete.jar -o ../PyImpl/Parser/libs -Dlanguage=Python3 -visitor ./fcssLexer.g4 ./fcssParser.g4

## Il write the rest later
```
