# -*- coding: utf-8 -*-
"""Contenido del tema 0, una sesion por nivel."""

# Hitos compartidos por los dos niveles. El texto largo cambia segun el curso.
HITOS = [
    dict(id='piedra', pos=0.02,  ep=u'2,6 M a&ntilde;os', t=u'La piedra tallada',
         c2=u'Un canto rodado golpeado contra otro hasta sacarle filo. Con eso se cortaba carne que los dientes no pod&iacute;an. No es poca cosa: es la primera vez que un ser vivo <b>fabrica una herramienta para fabricar otra cosa</b>.',
         c4=u'El canon olduvayense marca el inicio de la t&eacute;cnica: un gesto que se ense&ntilde;a y se repite. La herramienta deja de ser un objeto encontrado para ser un objeto <b>dise&ntilde;ado</b>, y el conocimiento de c&oacute;mo hacerla se transmite entre generaciones. Ah&iacute; empieza la cultura material.'),
    dict(id='fuego', pos=0.13, ep=u'800.000 a&ntilde;os', t=u'El dominio del fuego',
         c2=u'No lo inventaron: aprendieron a <b>conservarlo y encenderlo</b>. Con fuego se cocina (m&aacute;s energ&iacute;a de la misma comida), se alarga el d&iacute;a y se sobrevive al fr&iacute;o. Cambi&oacute; hasta la forma de nuestro cerebro.',
         c4=u'El fuego es la primera <b>fuente de energ&iacute;a controlada</b> ajena al m&uacute;sculo. Permite cocinar &mdash;lo que reduce el gasto digestivo y libera energ&iacute;a metab&oacute;lica para un cerebro mayor&mdash;, endurecer puntas de madera y, mucho despu&eacute;s, fundir metales. Toda la historia energ&eacute;tica posterior es una prolongaci&oacute;n de este control.'),
    dict(id='agri', pos=0.30, ep=u'10.000 a.C.', t=u'La agricultura',
         c2=u'Dejar de perseguir la comida y ponerla a crecer donde t&uacute; quieres. Aparecen las aldeas, los almacenes, los excedentes y, con ellos, los primeros oficios: si no todos cultivan, alguien puede dedicarse solo a hacer vasijas.',
         c4=u'La revoluci&oacute;n neol&iacute;tica introduce el <b>excedente</b>, y con &eacute;l la especializaci&oacute;n del trabajo, la propiedad, la jerarqu&iacute;a social y la escritura &mdash;que nace para contabilizar cosechas, no para hacer poes&iacute;a&mdash;. Es el primer caso claro de una tecnolog&iacute;a que reorganiza por completo la estructura social.'),
    dict(id='rueda', pos=0.42, ep=u'3.500 a.C.', t=u'La rueda y el metal',
         c2=u'La rueda no aparece para transportar: se usa primero como <b>torno de alfarero</b>. Y el cobre, el bronce y el hierro dan herramientas que no se rompen al primer golpe.',
         c4=u'La rueda es un caso de libro de <b>transferencia tecnol&oacute;gica</b>: nace como torno cer&aacute;mico y tarda siglos en aplicarse al transporte. La metalurgia, por su parte, exige hornos, miner&iacute;a y comercio a distancia: la primera cadena de suministro de la historia.'),
    dict(id='imprenta', pos=0.58, ep=u'1440', t=u'La imprenta',
         c2=u'Gutenberg no invent&oacute; la escritura ni el papel: invent&oacute; los <b>tipos m&oacute;viles</b>, letras sueltas reutilizables. De copiar un libro en un a&ntilde;o a imprimir cientos en una semana.',
         c4=u'La imprenta es la primera tecnolog&iacute;a de <b>reproducci&oacute;n en masa de informaci&oacute;n</b>. Derriba el monopolio del saber, hace posibles la Reforma y la Revoluci&oacute;n Cient&iacute;fica, y fija las lenguas nacionales. Compara su efecto con el de internet cinco siglos despu&eacute;s: el patr&oacute;n se repite.'),
    dict(id='vapor', pos=0.70, ep=u'1769', t=u'La m&aacute;quina de vapor',
         c2=u'Por primera vez una m&aacute;quina trabaja sin depender de un m&uacute;sculo, del viento o de un r&iacute;o. Nacen las f&aacute;bricas, el ferrocarril y las ciudades industriales. Es la <b>Primera Revoluci&oacute;n Industrial</b>.',
         c4=u'Watt no invent&oacute; la m&aacute;quina de vapor: le a&ntilde;adi&oacute; el condensador separado y multiplic&oacute; su rendimiento. Ese matiz importa, porque ilustra que <b>la innovaci&oacute;n suele ser mejora acumulativa</b>, no chispazo. Consecuencias: &eacute;xodo rural, proletariado urbano, y el arranque de la curva de CO&#8322; atmosf&eacute;rico.'),
    dict(id='electri', pos=0.82, ep=u'1870', t=u'Electricidad y cadena de montaje',
         c2=u'La energ&iacute;a ya viaja por un cable hasta donde la necesitas. Con el motor el&eacute;ctrico y la cadena de montaje, fabricar en serie se vuelve barato. <b>Segunda Revoluci&oacute;n Industrial</b>.',
         c4=u'La electricidad desacopla la producci&oacute;n de energ&iacute;a de su consumo, lo que reorganiza la f&aacute;brica entera. Sumada a la producci&oacute;n en cadena de Ford y a la qu&iacute;mica industrial, dispara la productividad y crea la <b>sociedad de consumo</b>, con su cara oculta: la obsolescencia y el residuo.'),
    dict(id='electro', pos=0.91, ep=u'1947-1971', t=u'El transistor y el chip',
         c2=u'Un interruptor sin piezas m&oacute;viles, min&uacute;sculo y barato. De ah&iacute; salen los ordenadores, y de los ordenadores, todo lo dem&aacute;s. <b>Tercera Revoluci&oacute;n Industrial</b>.',
         c4=u'El transistor (1947) y el microprocesador (1971) hacen la computaci&oacute;n barata y escalable. La ley de Moore &mdash;m&aacute;s una observaci&oacute;n econ&oacute;mica que una ley f&iacute;sica&mdash; describe un ritmo de mejora sin precedentes hist&oacute;ricos, y explica por qu&eacute; la tecnolog&iacute;a digital se difunde m&aacute;s r&aacute;pido que ninguna anterior.'),
    dict(id='digital', pos=0.985, ep=u'1990-hoy', t=u'Internet y la IA',
         c2=u'La informaci&oacute;n es lo que se produce y se transporta. El m&oacute;vil que llevas encima tiene m&aacute;s potencia que todos los ordenadores que llevaron al hombre a la Luna. <b>Cuarta Revoluci&oacute;n Industrial</b>.',
         c4=u'Digitalizaci&oacute;n, conectividad permanente, datos masivos e inteligencia artificial. Plantea problemas que las revoluciones anteriores no tuvieron: <b>brecha digital</b>, huella energ&eacute;tica de los centros de datos, privacidad, sesgos algor&iacute;tmicos y una velocidad de cambio que supera la capacidad de regulaci&oacute;n.'),
]

NIVELES = {
 '2eso': dict(
    curso=u'2.&ordm; de ESO', materia=u'Tecnolog&iacute;a y Digitalizaci&oacute;n',
    ruta='2eso/TyD/tema0/', arriba='../', sube2='../../', sube3='../../../',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">2.&ordm; ESO</a> &middot; <a href="../">TyD</a> &middot; Tema 0',
    titulo=u'Tema 0 &middot; &iquest;Qu&eacute; es la tecnolog&iacute;a?',
    h1=u'&iquest;Qu&eacute; es la tecnolog&iacute;a?',
    desc=u'Tema 0 de Tecnolog&iacute;a y Digitalizaci&oacute;n de 2.&ordm; de ESO: qu&eacute; es la tecnolog&iacute;a, en qu&eacute; se diferencia de la t&eacute;cnica y de la ciencia, y c&oacute;mo ha cambiado la historia desde la piedra tallada hasta la inteligencia artificial.',
    entradilla=u'Antes de dibujar, programar o construir nada, conviene saber de qu&eacute; estamos hablando. Esta sesi&oacute;n responde a una pregunta que parece f&aacute;cil y no lo es.',
    chips=[u'CE1 &middot; 1.1', u'A.1'],
    nivel_txt=u'2.&ordm; ESO'),
 '4eso': dict(
    curso=u'4.&ordm; de ESO', materia=u'Tecnolog&iacute;a',
    ruta='4eso/Tecnologia/tema0/', arriba='../', sube2='../../', sube3='../../../',
    migas=u'<a href="../../../">Materiales</a> &middot; <a href="../../">4.&ordm; ESO</a> &middot; <a href="../">Tecnolog&iacute;a</a> &middot; Tema 0',
    titulo=u'Tema 0 &middot; Tecnolog&iacute;a, t&eacute;cnica y sociedad',
    h1=u'Tecnolog&iacute;a, t&eacute;cnica y sociedad',
    desc=u'Tema 0 de Tecnolog&iacute;a de 4.&ordm; de ESO: definici&oacute;n de tecnolog&iacute;a, su relaci&oacute;n con la t&eacute;cnica y la ciencia, y an&aacute;lisis de su papel como motor de los cambios hist&oacute;ricos.',
    entradilla=u'Una sesi&oacute;n para fijar el vocabulario del curso y, sobre todo, para entender que la tecnolog&iacute;a no es un cat&aacute;logo de aparatos: es una forma de resolver problemas que ha reescrito la historia varias veces.',
    chips=[u'CE1 &middot; 1.1', u'CE5 &middot; 5.2', u'A.1'],
    nivel_txt=u'4.&ordm; ESO'),
}
