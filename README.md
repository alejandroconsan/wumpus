INSTRUCCIONES
=============

El código está desarrolldo sobre python 3.7.

En esta versión la manera de variar los parámetros del juego es modificando las variables directamente en el código, que por defecto son: 
ROW_NUMBER = 10
COLUMN_NUMBER = 10
HOLE_NUMBER = 10
ARROWS = 5

El personaje aparece siempre en la esquina superior izquierda del tablero mirando hacia abajo. El oro, los agujeros y el Wumpus se sitúan cada vez de una manera distinta a la anterior. El sistema de referencia se establece en la esquina superior izquierda y avanza de derecha aabajo.

El personaje atiende a 4 órdendes:
MOVE. Con esto avanza en la dirección en la que está mirando una casilla.
COUNTERCLOCKWISE. Gira sobre la misma casilla 90º en dirección antihoraria.
CLOCKWISE. Gira sobre la misma casilla 90º en dirección horaria.
SHOOT. Dispara una flecha en la dirección en la que está mirando (si le quedan).
EXIT. Permite salir del mapa, pero solo si está en la casilla de salida con el oro recogido.
