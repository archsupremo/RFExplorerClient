#!/usr/bin/python

def obtener_datos_x(index, datosx):
    for i in range(len(datosx)):
        if datosx[i] > index:
            return i-1

def mouseMoved(evt, grafica_plot, curva, vb, min_feq, max_feq, vLine):
    pos = evt[0]
    if grafica_plot.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        if index > float(min_feq) and index < float(max_feq):
            x,y = curva.getData()
            res =  y[obtener_datos_x(index, x)]
            grafica_plot.setLabel('top', "<span style='font-size: 12pt'>x=%0.1f, <span style='color: red'>y=%0.1f</span>" % (mousePoint.x(), res))
        vLine.setPos(mousePoint.x())
        #hLine.setPos(mousePoint.y())


# Para generar un histograma. No olvidar.
"""
for i, res in enumerate(resultados):
    if res != '':
        frequency_signal = res.split("\t")

        datos = [frequency_signal[0]]

        multiplicador = 120 - int(float(frequency_signal[1])) * -1
        vals = np.hstack([datos] * multiplicador)

        y, x = np.histogram(vals, bins=np.linspace(float(min_feq), float(max_feq), 150))

        grafica_plot.plot(x, y - 120, stepMode=True, fillLevel=0, brush=(0, 0, 0, 0))
"""
