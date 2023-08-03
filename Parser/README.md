## Compiling and using the parser

### Compiling
```sh
git clone https://github.com/PixelatedLagg/fcss/

cd fcss/Grammar
java -jar ../Jars/antlr-4.13.0-complete.jar -Dlanguage=Cpp -o ../Parser/libs -visitor fcssLexer.g4 fcssParser.g4

cd ../Parser/cmake
cmake ../
make all

## Use fcssParser executable
```
