default: states.svg states.png
	open states.png
	open -a "Google Chrome.app" states.svg

states.svg : states.dot
	dot -Tsvg states.dot > states.svg

states.png : states.dot
	dot -Tpng states.dot > states.png

states.dot : states.py
	./states.py --balls=3 --maxThrow=5 > states.dot

clean :
	rm *.dot *.svg *.png

