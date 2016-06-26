#Hamming syndrom steganography#

If you intend to execute the code, please make sure that numpy, PIL, and matplotlib are installed and usable from python interpreter.

This is a repository which contains what is useful in order to hide a message through hamming syndrom steganography.
It contains :

-a directory data which contains testing images

-a directory simple_LSB which contains a hide.py file and a reveal.py file, which use the content in utils directory in order to hide/reveal a message through simple LSB

-a directory hamming_LSB which contains a hide.py file and a reveal.py file, which use the content in utils directory in order to hide/reveal a message through LSB with Hamming syndrom

-a directory comparaison which contains tools and programs which are used in order to show that hamming syndrom LSB is far better than simple LSB (for example you can type
```shell
./histogram_comparaison.py  ../data/cosmos.png ../hamming_LSB/hamming_lsb_cosmos.png  ../simple_LSB/classical_lsb_cosmos.png
```
in the directory and see generated hsitograms).
In the subdirectory "example" of comparaison, there is a file named generation which contains command examples

-a directory utils which contains useful functions for LSB directories

-a directory other which contains fun images and other steano games with solutions

-a hide.py and reveal.py program (which are the same as in hamming_LSB dir)

-a ipython notebook which allow you to have a better understanding of what happen
