# Practica3 
Nos encontramos en el readme de la práctica 3 de programación paralela. La cual ha consistido en crear un juego en el que hay dos jugadores que tienen poder de actuación 
y pueden observar los cambios que van ocurriendo. 
Hemos realizado dos tipos de juego que explicaremos a continuación. 
1. El primero se trata de un juego en el que la temática es perseguir la bola. Los cohetes (jugadores) van en busca de la estrella (bola). Cuando consigue uno de ellos atraparla obtiene un punto. La competición consiste en atrapar la bola la mayor cantidad de veces posibles para obtener la máxima puntuación de los dos jugadores y ganar. 
El juego tiene una dificultad, cada vez que un jugador alcanza 5 puntos o un múltiplo de él, la velocidad de la bola aumenta. Así será más difícil de atraparla y los 
jugadores se tendrán que esforzar más para obtener puntos.  
En cuanto a este apartado tenemos los siguientes archivos: 
  -sala2.py: 
  -player.py: 
  -espacio2.png: Se trata del fondo del tablero de juego. Hemos elegido el espacio para que cuadre con la temática de los cohetes y la estrella. 
  
2.El segundo juego tiene la temática de esquivar las distintas bolas. Los astronautas (jugadores) deben esquivar los distintos meteoritos (bolas). Cuando un meteorito 
 consigue darle a un jugador, el otro consigue un punto. Cuantas más veces consigan los meteoritos dar a un jugador más puntos consigue el contrario. La competición     consiste en ser el más hábil que el contario esquivando. 
 En este caso, también tenemos que el juego consta de una dificultad. Cuando uno de los jugadores llega a 10 o a un múltiplo de él, solo la última bola que ha tocado     al jugador aumenta la velocidad. Así las distintas bolas tendrán distintas velocidades y será más complicado cada vez esquivarlas. 
 En cuanto a este apartado tenemos los siguientes archivos: 
   -sala_esq: 
   -player_esq: 
   -planet.png: Se trata del fondo del tablero de juego en esta versión. Se ve un planeta que encaja con la temática seguida en este caso de astronautas y meteoritos.  

Por último explicamos la carpeta llamada img. Esta carpeta contiene las imágenes usadas para los jugadores y las bolas en las distintas versiones del juego. 
-nave.png: son los jugadores del primer juego. Son cohetes que buscan su estrella. 
-estrella.png: es la bola del primer juego. Esta es una estrella que debe ser capturada por los cohetes. 
-astr.png: se trata de los jugadores del segundo juego. Son unos astronautas que deben esquivar los meteoritos del espacio para sobrevivir. 
-meteor.png: estamos ante las bolas del segundo juego. Estos meteoritos se chocan con todo y deben ser esquivados. 
