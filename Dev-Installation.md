# Installing FCSS yourself

## Python Implementation
```sh
git clone https://github.com/PixelatedLagg/fcss/
cd fcss/Grammar

## Compile grammar
java -jar ../Jars/antlr-4.13.0-complete.jar -o ../PyImpl/Parser/libs -Dlanguage=Python3 -visitor ./fcssLexer.g4 ./fcssParser.g4

## Now you can run the parser!
cd ../PyImpl/Parser
python main.py styles.fcss
## Tada you now have a parsed fcss instruction set!

## TODO: Write the example for executing with html :>
## Maybe like:
## python main.py -html my_program.html styles.fcss
## Outputs node files ?
```
