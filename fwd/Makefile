#!/usr/bin/make -f

CC=gcc
CFLAGS=-Wall -Wextra -Werror
OUT=fwd

fwd.o:
	$(CC) fwd.c -o $(OUT) $(CFLAGS)

all: fwd.o

install: all
	chown root:root $(OUT)
	chmod 4755 $(OUT)
	mv $(OUT) /usr/local/bin

clean:
	rm -f $(OUT)


