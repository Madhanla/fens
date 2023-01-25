# Ejemplos de uso de `fen.py'
* Posición inicial
~~~
python3 fen.py 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
~~~
Salida:
~~~
{{Diagrama de ajedrez
|
|
|=
 8 |rd|nd|bd|qd|kd|bd|nd|rd|=
 7 |pd|pd|pd|pd|pd|pd|pd|pd|=
 6 |  |  |  |  |  |  |  |  |=
 5 |  |  |  |  |  |  |  |  |=
 4 |  |  |  |  |  |  |  |  |=
 3 |  |  |  |  |  |  |  |  |=
 2 |pl|pl|pl|pl|pl|pl|pl|pl|=
 1 |rl|nl|bl|ql|kl|bl|nl|rl|=
    a  b  c  d  e  f  g  h
|
}}
~~~

* Posición final Opera Game
~~~
python3 fen.py '1n1Rkb1r/p4ppp/4q3/4p1B1/4P3/8/PPP2PPP/2K5 b k - 1 17' --header='Hello%C5Wo%H8ld'  --footer -A tleft
~~~
Salida:
~~~
{{Diagrama de ajedrez
| tleft
| Hello World
|=
 8 |  |nd|  |rl|kd|bd|  |rd|=
 7 |pd|  |  |  |  |pd|pd|pd|=
 6 |  |  |  |  |qd|  |  |  |=
 5 |  |  |  |  |pd|  |bl|  |=
 4 |  |  |  |  |pl|  |  |  |=
 3 |  |  |  |  |  |  |  |  |=
 2 |pl|pl|pl|  |  |pl|pl|pl|=
 1 |  |  |kl|  |  |  |  |  |=
    a  b  c  d  e  f  g  h
| Las negras mueven
}}
~~~

* Combinación final Inmortal de Anderssen
~~~
python3 fen.py 'r1b1k1nr/p2p1ppp/n2B4/1p1NPN1P/6P1/3P1Q2/P1P1K3/q5b1 w kq - 2 21' --footer 'Las %s tienen ahora %m.Cxg7+! con mate en 3'
~~~
Salida:
~~~
{{Diagrama de ajedrez
|
|
|=
 8 |rd|  |bd|  |kd|  |nd|rd|=
 7 |pd|  |  |pd|  |pd|pd|pd|=
 6 |nd|  |  |bl|  |  |  |  |=
 5 |  |pd|  |nl|pl|nl|  |pl|=
 4 |  |  |  |  |  |  |pl|  |=
 3 |  |  |  |pl|  |ql|  |  |=
 2 |pl|  |pl|  |kl|  |  |  |=
 1 |qd|  |  |  |  |  |bd|  |=
    a  b  c  d  e  f  g  h
| Las blancas tienen ahora 21.Cxg7+! con mate en 3
}}
~~~
