TEX=pdflatex

.PHONY: all
all: ps1.pdf ps2.pdf

ps1.pdf: ps1.tex
	${TEX} ps1.tex

ps2.pdf: ps2.tex
	${TEX} ps2.tex