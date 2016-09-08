APP     = flowmon

SRCDIR  = src/
BINDIR  = bin/

SRCS    := $(shell find $(SRCDIR) -name '*.cc' -exec basename {} \;)
#SRCS    := $(wildcard $(SRCDIR)/*.cc)
SRCDIRS := $(shell find . -name '*.c' -exec dirname {} \; | uniq)
OBJS    := $(patsubst %.cc,$(BINDIR)/%.o,$(SRCS))
#OBJS    := $(OBJ:.cc=$(OBJDIR)/.o)

CC = g++
CFLAGS  = -g -Wall 
curr_dir = $(shell pwd)
LIBS = -L $(curr_dir)/../../lib/mongocxx -lmongoclient -lyaml-cpp -lboost_thread -lboost_system -lboost_regex
INC = -I $(curr_dir)/../../lib/mongocxx/include/ -I $(SRCDIR) 

all:  directories $(BINDIR)/$(APP)

directories:
	mkdir -p bin

$(BINDIR)/$(APP) : $(OBJS)
		$(CC) $(OBJS) $(LIBS) -pthread -o $@

$(BINDIR)/%.o: $(SRCDIR)/%.cc
		$(CC) $(CFLAGS) $(INC) -c $< -o $@

clean:
	rm bin/*
#buildrepo:
#		@$(call make-repo)

#define make-repo
#   for dir in $(SRCDIRS); \
#          do \
#	  	mkdir -p $(OBJDIR)/$$dir; \
#		   done
#   endef
