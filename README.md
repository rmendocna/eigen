# A command line utility that calculates the word frequency distribution for the text files 
within a given folder.

#### to install (posix)
1. checkout the repo
```
$ git clone https://github.com/rmendocna/word_freq_dist.git
``` 

2. Setup a virtual environment
```
$ cd word_freq_dist
word_freq_dist$ python3 -mvenv .
(word_freq_dist)word_freq_dist$ . bin/activate
```
3. run
```
(word_freq_dist)word_freq_dist$ python most_frequent.py docs
Wrote freq_dist.html
(word_freq_dist)word_freq_dist$
```
4. Open `freq_dist.html` on your browser

5. There is an additional option `-p` to generate the output in PDF format, which is made available if you install the `reportlab` package.

  Not an actual requirement.
