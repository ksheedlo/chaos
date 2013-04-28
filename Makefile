TEX=pdflatex

.PHONY: all
all: ps1.pdf ps2.pdf ps3.pdf ps4.pdf ps5.pdf ps6.pdf ps7.pdf ps8.pdf ps9.pdf ps10.pdf ps12.pdf

%.pdf: %.tex 
	${TEX} $^