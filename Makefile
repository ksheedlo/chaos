TEX=pdflatex

.PHONY: all
all: ps1.pdf ps2.pdf ps3.pdf ps4.pdf ps5.pdf ps6.pdf ps7.pdf ps8.pdf ps9.pdf ps10.pdf

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

ps6.pdf: ps6.tex 
	${TEX} ps6.tex

ps7.pdf: ps7.tex 
	${TEX} ps7.tex

ps8.pdf: ps8.tex 
	${TEX} ps8.tex

ps9.pdf: ps9.tex 
	${TEX} ps9.tex

ps10.pdf: ps10.tex
	${TEX} ps10.tex