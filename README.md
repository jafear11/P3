PAV - P3: estimación de pitch
=============================

Esta práctica se distribuye a través del repositorio GitHub [Práctica 3](https://github.com/albino-pav/P3).
Siga las instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para realizar un `fork` de la
misma y distribuir copias locales (*clones*) del mismo a los distintos integrantes del grupo de prácticas.

Recuerde realizar el *pull request* al repositorio original una vez completada la práctica.

Ejercicios básicos
------------------

- Complete el código de los ficheros necesarios para realizar la estimación de pitch usando el programa
  `get_pitch`.

   * Complete el cálculo de la autocorrelación e inserte a continuación el código correspondiente.
   ```
void PitchAnalyzer::autocorrelation(const vector<float> &x, vector<float> &r) const
  {

    for (unsigned int l = 0; l < r.size(); ++l)
    {
      r[l] = 0;
      for (unsigned int n = l; n < x.size(); n++)
      {
        r[l] += x[n] * x[n - l];
      }
      r[l] /= x.size();
    }

    if (r[0] == 0.0F) // to avoid log() and divide zero
      r[0] = 1e-10;
  }
	```
	
   * Inserte una gŕafica donde, en un *subplot*, se vea con claridad la señal temporal de un segmento de
     unos 30 ms de un fonema sonoro y su periodo de pitch; y, en otro *subplot*, se vea con claridad la
	 autocorrelación de la señal y la posición del primer máximo secundario.

	 NOTA: es más que probable que tenga que usar Python, Octave/MATLAB u otro programa semejante para
	 hacerlo. Se valorará la utilización de la biblioteca matplotlib de Python.
	
	INSERTAAAAR !!!

   * Determine el mejor candidato para el periodo de pitch localizando el primer máximo secundario de la
     autocorrelación. Inserte a continuación el código correspondiente.
	
	```
float PitchAnalyzer::compute_pitch(vector<float> &x) const
  {
    if (x.size() != frameLen)
      return -1.0F;

    for (unsigned int i = 0; i < x.size(); ++i)
      x[i] *= window[i];
    clip_center(x, 0.01);
    normalize(x);

    vector<float> r(npitch_max);

    autocorrelation(x, r);

    vector<float>::const_iterator iR = r.begin(), iRMax = iR;
    for (iR = iRMax = r.begin() + npitch_min; iR < r.begin() + npitch_max; iR++)
    {
      if (*iR > *iRMax)
      {
        iRMax = iR;
      }
    }
    unsigned int lag = iRMax - r.begin();

    float pot = 10 * log10(r[0]);

#if 0
    if (r[0] > 0.0F)
      cout << pot << '\t' << r[1]/r[0] << '\t' << r[lag]/r[0] << endl;
#endif

    if (unvoiced(pot, r[1] / r[0], r[lag] / r[0]))
      return 0;
    else
      return (float)samplingFreq / (float)lag;
  }
}
```	
   * Implemente la regla de decisión sonoro o sordo e inserte el código correspondiente.
	
<img width="608" alt="image" src="https://user-images.githubusercontent.com/100561275/163795027-ed273760-6ea1-4d6e-9391-59c779f5534b.png">

		  
- Una vez completados los puntos anteriores, dispondrá de una primera versión del estimador de pitch. El 
  resto del trabajo consiste, básicamente, en obtener las mejores prestaciones posibles con él.

  * Utilice el programa `wavesurfer` para analizar las condiciones apropiadas para determinar si un
    segmento es sonoro o sordo. 
	
	  - Inserte una gráfica con la estimación de pitch incorporada a `wavesurfer` y, junto a ella, los 
	    principales candidatos para determinar la sonoridad de la voz: el nivel de potencia de la señal
		(r[0]), la autocorrelación normalizada de uno (r1norm = r[1] / r[0]) y el valor de la
		autocorrelación en su máximo secundario (rmaxnorm = r[lag] / r[0]).

		Puede considerar, también, la conveniencia de usar la tasa de cruces por cero.

	    Recuerde configurar los paneles de datos para que el desplazamiento de ventana sea el adecuado, que
		en esta práctica es de 15 ms.
		  
		  INSERTAAAR GRAAFICA!!

      - Use el estimador de pitch implementado en el programa `wavesurfer` en una señal de prueba y compare
	    su resultado con el obtenido por la mejor versión de su propio sistema.  Inserte una gráfica
		ilustrativa del resultado de ambos estimadores.
     
		Aunque puede usar el propio Wavesurfer para obtener la representación, se valorará
	 	el uso de alternativas de mayor calidad (particularmente Python).
		  
		  INSETAAR GRAFICA!!
  
  * Optimice los parámetros de su sistema de estimación de pitch e inserte una tabla con las tasas de error
    y el *score* TOTAL proporcionados por `pitch_evaluate` en la evaluación de la base de datos 
	`pitch_db/train`..
		  
<img width="376" alt="image" src="https://user-images.githubusercontent.com/100561275/163777778-8e52a046-459a-42d1-a4e3-deefa209efec.png">


Ejercicios de ampliación
------------------------

- Usando la librería `docopt_cpp`, modifique el fichero `get_pitch.cpp` para incorporar los parámetros del
  estimador a los argumentos de la línea de comandos.
  
  Esta técnica le resultará especialmente útil para optimizar los parámetros del estimador. Recuerde que
  una parte importante de la evaluación recaerá en el resultado obtenido en la estimación de pitch en la
  base de datos.

  * Inserte un *pantallazo* en el que se vea el mensaje de ayuda del programa y un ejemplo de utilización
    con los argumentos añadidos.
	
	FER DOCOOOPT!!!!

- Implemente las técnicas que considere oportunas para optimizar las prestaciones del sistema de estimación
  de pitch.

  Entre las posibles mejoras, puede escoger una o más de las siguientes:

  * Técnicas de preprocesado: filtrado paso bajo, diezmado, *center clipping*, etc.
		  ```
void PitchAnalyzer::clip_center(vector<float> &x, float xth) const
  {
    for (int i = 0; i < x.size(); i++)
    {
      if (abs(x[i]) < xth)
      {
        x[i] = 0;
      }
      else if (x[i] < 0)
      {
        x[i] += xth;
      }
      else
        x[i] += xth;
    }
  }
void PitchAnalyzer::normalize(vector<float> &x) const
  {
    float max = 0;
    for (int i = 0; i < x.size(); i++)
    {
      if (x[i] > max)
      {
        max = x[i];
      }
    }
    for (int i = 0; i < x.size(); i++)
    {
      x[i] /= max;
    }
  }
				 ```
				 
  * Técnicas de postprocesado: filtro de mediana, *dynamic time warping*, etc.
				 
				 ```
void median_filter(vector<float> &pitches)
{
  vector<float> sorted = pitches;
  vector<float> sorting = pitches;
  float a;
  for (int i = 1; i < pitches.size() - 1; i++)
  {
    sorting[0] = pitches[i - 1];
    sorting[1] = pitches[i];
    sorting[2] = pitches[i + 1];
    for (int j = 0; j < 2; j++)
    {
      for (int k = 0; k < 2; k++)
      {
        if (sorting[k] > sorting[k + 1])
        {
          a = sorting[k + 1];
          sorting[k + 1] = sorting[k];
          sorting[k] = a;
        }
      }
    }
    sorted[i] = sorting[1];
  }
  pitches = sorted;
}
	```

  * Métodos alternativos a la autocorrelación: procesado cepstral, *average magnitude difference function*
    (AMDF), etc.
  * Optimización **demostrable** de los parámetros que gobiernan el estimador, en concreto, de los que
    gobiernan la decisión sonoro/sordo.
  * Cualquier otra técnica que se le pueda ocurrir o encuentre en la literatura.

  Encontrará más información acerca de estas técnicas en las [Transparencias del Curso](https://atenea.upc.edu/pluginfile.php/2908770/mod_resource/content/3/2b_PS%20Techniques.pdf)
  y en [Spoken Language Processing](https://discovery.upc.edu/iii/encore/record/C__Rb1233593?lang=cat).
  También encontrará más información en los anexos del enunciado de esta práctica.

  Incluya, a continuación, una explicación de las técnicas incorporadas al estimador. Se valorará la
  inclusión de gráficas, tablas, código o cualquier otra cosa que ayude a comprender el trabajo realizado.
	
	Hemos utilizado la técnica de preprocesado center clipping y la técnica de postprocesado filtro de mediana. Previamente, también hemos normalizado la señal.
	El center clipping consiste básicamente en anular los valores de la señal de magnitud pequeña. Con ello conseguimos dos cosas: al introducir una distorsión no lineal, aumentamos la intensidad de los armónicos de orden elevado y al poner a cero los instantes de tiempo donde la señal tiene amplitud menor, aumentamos robustez frente al ruido. A continuación adjuntamos el código del center clipping. Cabe comentar que curiosamente, pese a que hemos implementado el center clipping con offset, la fórmula utilizada no es exactamente la propuesta en el enunciado de la práctica, puesto que de esta forma el detector nos daba mejor SCORE total. Como podemos ver en el código adjunto más arriba, en el último else, se le suma el umbral a la muestra actual, en vez de restárselo.
	El filtro de mediana es un filtro no lineal que se basa en calcular el valor mediano en una ventana (de longitud 3 en nuestro caso) centrada en cada instante de tiempo. Lo usamos principalmente para evitar errores groseros en la estimación de la frecuencia de pitch. 
	



  También se valorará la realización de un estudio de los parámetros involucrados. Por ejemplo, si se opta
  por implementar el filtro de mediana, se valorará el análisis de los resultados obtenidos en función de
  la longitud del filtro.
   

Evaluación *ciega* del estimador
-------------------------------

Antes de realizar el *pull request* debe asegurarse de que su repositorio contiene los ficheros necesarios
para compilar los programas correctamente ejecutando `make release`.

Con los ejecutables construidos de esta manera, los profesores de la asignatura procederán a evaluar el
estimador con la parte de test de la base de datos (desconocida para los alumnos). Una parte importante de
la nota de la práctica recaerá en el resultado de esta evaluación.
