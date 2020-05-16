aname = digitAstar
idaname = digitIDAstar

all: stage initial uos

stage: $(aname)_stage.cpp
	g++ -o $(aname)_stage.out $(aname)_stage.cpp -Wall -O3 -g

initial: $(aname)_initial.cpp
	g++ -o $(aname)_initial.out $(aname)_initial.cpp -Wall -O3 -g
	
uos: $(aname)_unordered_set.cpp
	g++ -o $(aname)_unordered_set.out $(aname)_unordered_set.cpp -Wall -O3 -g

clean:
	rm *.out