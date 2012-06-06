from brian import *

tsim = 1000

vestibular_ganglion = PoissonGroup(100, rates=lambda t:exp(-(((t/msecond)-tsim/2)/(tsim/5))**2)*40*Hz)
#rates=lambda t: exp(-((t-tsim/2)/(tsim/5))^2)*10*Hz



M = SpikeMonitor(vestibular_ganglion)
run(tsim * msecond)
raster_plot(M)
show()
