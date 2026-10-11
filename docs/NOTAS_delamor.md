# NOTAS_delamor.md

*Sep 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

---

## Tema 1 — Distribución / sesgo estructural de W en sweeps count_attractors · P5–P7


BIAS1**"sesgo de uniformidad en σ₀"   implementado 3 modos de sampling para Monitor service y para COCO

BIAS 2 *sesgo de n_runs (coupon-collector)".en REG_count_attractors_bias_v1.


idea conceptual:
 
def _count_attractors(….) 
{
  return _count_invariant_sets(….)
 } 
  
  --------------------------------------------------------
  
  
  def _count_invariant_set(….)
  {
  	Xi = elemento de ciclo de cualquier orden  		<---ie: un estado State del modelo 
    	       			
  	circular_setx =	{X1,...,Xn}  es el conjunto de n elementos sin orden representa ciclo n =  X1 - ... - Xn - X1 
  				ie ciclo  2 de A-> B-> A : circular_setx = {A, B}
  
  	
  	invariant_set = conjunto (maximo) de circular_setx diferentes.(únicos) 	<---	L
  	  	
	realiza el sweep de relax actual bajo modo de sampling 
 		cada vez que se estabiliza (converge) a   un circular_setx =	{X1,...,Xn}
		  	si circular_setx es nuevo  (no tiene los mismos  elementos que ninguno de los sets ya identificados) 
  	 	 		invariant_set.add(circular_setx)

	persist(invariant_set.to_json)
	return invariant_set.count
   }


  ie:
   Caso 1 cada vez que converge a un ciclo 1  ie  A : el set ={A} conjunto de 1 elementos sin orden <- convergencia a conjunto fijo de 1 único elemento
   Caso 2 vez que converge a un ciclo 2  ie  A-B-A : el set ={A, B} conjunto de 2 elementos sin orden
   Caso 3cada vez que converge a un ciclo 3 ie  A-B-C-A : el set ={A, B, C} conjunto de 3 elementos sin orden
   ...
   
}

Criterios de diversidad: volumen de cuencas top-k  comparison

1. Armar TASK Criterios de diversidad: volumen de cuencas top-k 
2 Premisas Principio de Invarianza de LaSalle:
		 para los dominios 	
		 
		 Sea 
		 		W = matriz  config de  de pesos discreta,  simétrica, con diagonal cero (estados) 
		 		Sigma(W) = sigma estado de W  
		 		
		 
		 Se define:
		 		V(E) = L 
		 donde: 
		 		E = dominio de estados iniciales posibles de W  
		 		V = Función de mapeo por relax  activacion hopfield sincronica con Sigma 0 inicial aleatorio según sampling mode.
		 		
		 			V = A0 - Aactual       
		 		
		 			donde 
		 				A0 es  volumen de cuencas top-k(Sigama0(W))
		 				Aactual  es  volumen de cuencas top-k( Sigma actual(W))
		 				L  = conjunto  maximo invariante de E
		 				
		 		volumen de cuencas top-k
		 			
````		 			
		 				
3. driver que sostenga al REG que genera la task 

casos 
 
---
	## — Criterios de diversidad: conteo de atractores, coercividad, cuencas (abierto)
	
	**Qué hay que trabajar en el paper:**
	El paper usa "attractor diversity" como concepto pero no lo define formalmente. ¿Qué es diversidad en CKM? ¿Conteo de atractores únicos? ¿Tamaño de cuencas? ¿Coercividad? ¿Los tres son complementarios o redundantes?
	
	**Estado actual:**
	- Conteo de atractores (A): implementado, metodología en revisión (ver Tema 1)
	- Coercividad: verificada geométricamente en lazo P1. Definición operativa: valor de ρ donde c(S) cruza cero en rama UP. Es un intervalo frustrado [0.406, 0.586], no un punto.
	- Cuencas: propuesto que son pequeñas y profundas en sistema frustrado. No verificado directamente.
	
	**La pregunta abierta:**
	¿Son A (conteo), coercividad, y tamaño de cuencas tres medidas del mismo fenómeno o tres dimensiones independientes de "diversidad"? ¿Puede el paper proponer un criterio unificado?

**Referencias:**
- `REG_mapeo_magnetico_ckm_v1.md §1.7` — coercividad CKM, lazo P1, datos disponibles en hopfield.py
- `DEFS_CKM_estado_actual_v3.md §3` — coercividad como intervalo
- `PAPER v11 §5.3` — P4 / W_mixta coercividad
- `REG_stochastic_eval_v2.md` — A_observed bajo dos modos, ninguno validado
- `Thermodynae_Link.pdf` — Husain (2026) Eur. Phys. J. B: transición de fase continua en red Hopfield memristiva. Atención: aplica a Hopfield asociativo estándar, no directamente a CKM. El paper de Husain muestra ausencia de histeresis → transición continua. CKM muestra histeresis (P1) → régimen distinto.

**Riesgo de confusión:**
- No equiparar "atractor único" con "cuenca grande". En sistemas frustrados las cuencas más profundas pueden ser las más pequeñas en extensión.
- No usar Husain (2026) para argumentar sobre N mínimo de CKM — ver DEFS v3 §14.

---

## Tema 4 — Néel (≈ Nielsen ≈ TEER) · selección dinámica de pares negativos

**Qué es:**
Temperatura de Néel efectiva como criterio de elicitación de pares negativos sin sesgo externo. Louis Néel, físico. El nombre fue aproximado en sesión como "Nielsen" y "TEER" — la unión de los dos términos delimita el concepto exacto.

**El criterio** (propuesto, no verificado — DEFS_CKM_estado_actual_v3.md §12):
1. Construir W_pos sin declarar pares negativos.
2. Barrer β de alto a bajo.
3. Medir separabilidad T0 vs T1 en cada β: c(S) interno vs cruzado.
4. β_Néel = β donde la separabilidad colapsa.
5. Los pares (i,j) en clusters opuestos antes del colapso → candidatos a pares negativos.

Criterio estructural, no editorial. Los pares emergen del barrido.

**Referencias:**
- `DEFS_CKM_estado_actual_v3.md §12`
- `REG_mapeo_magnetico_ckm_v1.md §3.3`
- `PAPER v11 §2.3`

---

---

*gadanindelamor/ckm — Septiembre 2026*
