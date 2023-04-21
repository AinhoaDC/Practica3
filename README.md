# Practica3 
El objetivo de esta práctica es crear un código de programación distributiva a través del cual se generará un juego.
En nuestro caso, hemos realizado dos tipos de juego, uno más sencillo y otro creado a partir del anterior, que explicaremos a continuación:

1. "Atrapa la estrella": se trata de un juego en el que la temática es perseguir la bola. Los jugadores, que estarán representados por naves espaciales, deben ir en busca de la estrella (bola), pudiéndose mover por todo el tablero. Cuando consigue uno de ellos atraparla obtiene un punto y la bola se reubicará en una nueva posición aleatoria. La competición consiste en atrapar la bola la mayor cantidad de veces posibles para obtener la máxima puntuación de los dos jugadores y ganar. 
El juego irá aumentando de dificultad a medida que se desarrollan los acontecimientos: cada vez que alguno de los jugadores alcanza 5 puntos o un múltiplo de él, la velocidad de la estrella aumenta. Así será más complicado atraparla y los jugadores se tendrán que esforzar más para obtener puntos.  
Para este apartado utilizaremos los siguientes archivos, que contienen los códigos necesarios para que el juego funcione, así como la imagen para el fondo del tablero: 
  
      -sala2.py: Este archivo contiene el código de la implementación de la sala del primer juego.
  
      -player.py: El archivo denominado así contiene el código de python de los jugadores del primer juego.
  
      -espacio2.png: Se trata del fondo del tablero de juego. Hemos elegido el espacio para que cuadre con la temática de los cohetes y la estrella. 
  
2. "Esquiva el meteorito": este juego tiene el objetivo de esquivar las distintas bolas, que está representadas, en este caso por meteoritos. Como ya adelanta en la frase anterioir, la principal diferencia de una juego repecto al otro es, además de tener objetivos distintos, que en este juego hay más de una bola (habrá 6 bolas, en concreto). Los jugadores estarán representados por imágenes de astronautas y s mueven por todo el tablero tratando de, como hemos dicho, esquivar los meteoritos. Cuando un meteorito 
consigue darle a un jugador, el contrario consigue un punto y el meteorito que ha colisionado desaparecerá y aparecerá en una nueva posición completamente aleatoria, al igual que en "Atrapa la bola". Cuantas más veces consigan los meteoritos dar a un jugador más puntos consigue el contrario. La competición consiste en ser el más hábil que el contario esquivando. 
En este caso, también tenemos que el juego consta de una dificultad. Cuando uno de los jugadores llega a 10 o a un múltiplo de él, solo la última bola que ha tocado    al jugador aumenta la velocidad. Así las distintas bolas tendrán distintas velocidades y será más complicado cada vez esquivarlas. 
En cuanto a este apartado tenemos los siguientes archivos: 
  
      -sala_esq: Este archivo contiene el código de python de la sala del segundo juego.
  
      -player_esq: El archivo denominado así contiene el código de la implementación de los jugadores del segundo juego. 
  
      -planet.png: Se trata del fondo del tablero de juego en esta versión. Se ve un planeta que encaja con la temática seguida en este caso de astronautas y meteoritos.  

Además, en este git tenemos la carpeta llamada img. Esta carpeta contiene las imágenes usadas para los sprites de los jugadores y las bolas en las distintas versiones del juego. 
  
  -nave.png: son los jugadores del primer juego. Son cohetes que buscan su estrella. 
  
  -estrella.png: es la bola del primer juego. Esta es una estrella que debe ser capturada por los cohetes. 
  
  -astr.png: se trata de los jugadores del segundo juego. Son unos astronautas que deben esquivar los meteoritos del espacio para sobrevivir. 
  
  -meteor.png: estamos ante las bolas del segundo juego. Estos meteoritos se chocan con todo y deben ser esquivados. 
