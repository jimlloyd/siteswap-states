states.svg : states.dot
	dot -Tsvg states.dot > states.svg

states.dot : states.py
	./states.py --balls=3 --maxThrow=5 --pattern=51 > states.dot

clean :
	rm *.dot *.svg
