TEX=pdflatex

.PHONY: all
all: ps1.pdf ps2.pdf ps3.pdf ps4.pdf ps5.pdf

ps1.pdf: ps1.tex
	${TEX} ps1.tex

ps2.pdf: ps2.tex
	${TEX} ps2.tex

ps3.pdf: ps3.tex
	${TEX} ps3.tex

ps4.pdf: ps4.tex
	${TEX} ps4.tex

ps5.pdf: ps5.tex
	${TEX} ps5.tex