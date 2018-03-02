# Overview

This utility allows you to prepare your e-book file to a specified screen size
of your e-reader or tablet PC using TeX markup system. 
Input file format should be FB2, output file format is .tex, that you can
transform to PDF using texlive or another TeX distro.

# Basic usage
Clone the repo:
```
git clone https://github.com/greensk/fb2-to-tex.git
```
use file `run.py` to conver books to TeX.
```
./run.py --paperwidth=5cm --paperheight=7cm war_and_pease.fb2.zip war_and_prase.tex
```

# Book file prepare flow

1. Installation a LaTeX distro. Here is an example for Debian/Ubuntu.
```
sudo apt-get install texinfo texlive texlive-fonts-extra
```
Maybe necessary to install a localization package:
```
sudo apt-get install texlive-lang-cyrillic
```

2. Calculate for mobile device screen width and height.
3. Use the utility to prapre your book for a specified screen size.
4. Convert the output .tex file to PDF using LaTeX command:
```
texi2pdf -c war_and_prase.tex war_and_prase.pdf
```
5. Load the prepared PDF to your mobile device.
6. Enjoy a good formatted e-book.
