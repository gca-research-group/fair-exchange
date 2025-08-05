# compilar o arquivo .pml e gerar o arquivo pan.c
spin -a alice.pml

# compilar o arquivo pan.c para gerar o executável pan.exe
gcc -o pan ./pan.c

# executar o modelo com o pan.exe
./pan.exe -a -e -c500
