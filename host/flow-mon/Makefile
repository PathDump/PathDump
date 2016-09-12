APP     = flowmon

SRCDIR  = src/
BINDIR  = bin/

SRCS    := $(shell find $(SRCDIR) -name '*.cc' -exec basename {} \;)
#SRCS    := $(wildcard $(SRCDIR)/*.cc)
SRCDIRS := $(shell find . -name '*.c' -exec dirname {} \; | uniq)
OBJS    := $(patsubst %.cc,$(BINDIR)/%.o,$(SRCS))
CC = c++
CFLAGS  = -g -Wall --std=c++11 
curr_dir = $(shell pwd)
LIBS = -L/usr/local/lib -lmongoclient -lyaml-cpp -lboost_thread -lboost_system -lboost_regex
INC = -I $(SRCDIR)

all:  directories $(BINDIR)/$(APP)

directories:
	mkdir -p bin

$(BINDIR)/$(APP) : $(OBJS)
		$(CC) $(OBJS) $(LIBS) -pthread -o $@ 

$(BINDIR)/%.o: $(SRCDIR)/%.cc
		$(CC) $(CFLAGS) $(INC) -c $< -o $@

clean:
	rm bin/*
