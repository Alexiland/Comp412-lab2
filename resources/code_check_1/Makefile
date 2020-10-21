# Makefile for the COMP 412, Lab 1, code checking tools
CFLAGS=-Wall -O2

tools:	ReportOne CheckOne

ReportOne:	ReportOne.c
	gcc $(CFLAGS) ReportOne.c
	mv a.out ReportOne

CheckOne:	CheckOne.c
	gcc $(CFLAGS) CheckOne.c
	mv a.out CheckOne

export:	Makefile README CheckOne.c ReportOne.c CodeCheck1 CodeCheckHelper
	tar cvf export.tar Makefile README *.c CodeCheck1 CodeCheckHelper

clean:	
	rm -i *~ CheckOne ReportOne
