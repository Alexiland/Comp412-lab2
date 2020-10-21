# Makefile for the COMP 412, Lab 2, code checking tools
CFLAGS=-Wall -O2

tools:	CheckResults AllocOne 

CheckResults:	CheckResults.c
	gcc $(CFLAGS) CheckResults.c
	mv a.out CheckResults

AllocOne:	AllocOne.c
	gcc $(CFLAGS) AllocOne.c
	mv a.out AllocOne

export:	Makefile README AllocOne.c CheckResults.c CodeCheck2 CC2Helper
	tar cvf export.tar Makefile README *.c CodeCheck2 CC2Helper \
		cc*i

clean:	
	rm -i *~ CheckResults AllocOne 
