echo on
set path=%1
::don't forget to add %path% for your compilation command!
:: example - g++ %path%/main.cpp -o %path%/main

g++ %path%/main.cpp -o %path%/main