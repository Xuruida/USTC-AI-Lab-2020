aname = digitAstar
idaname = digitIDAStar

all: stage initial uos ida

stage: $(aname)_stage.cpp
	g++ -o $(aname)_stage $(aname)_stage.cpp -Wall -O3 -g

initial: $(aname)_initial.cpp
	g++ -o $(aname)_initial $(aname)_initial.cpp -Wall -O3 -g
	
uos: $(aname)_unordered_set.cpp
	g++ -o $(aname)_unordered_set $(aname)_unordered_set.cpp -Wall -O3 -g

ida: $(idaname).cpp
	g++ -o $(idaname) $(idaname).cpp -Wall -O3 -g

clean:
	rm *.out