import backtrader as bt
import backtrader.plot as btplot

class MyCerebro(bt.Cerebro):
    def plot(self, plotter=None, numfigs=1, iplot=True,
             start=None, end=None, width=30, height=10,
             dpi=300, tight=True, use=None, **kwargs):

        if self._exactbars > 0:
            return
        
        kwargs['figsize'] = (width, height)
        kwargs['dpi'] = dpi

        if not plotter:
            if self.p.oldsync:
                plotter = btplot.Plot_OldSync(**kwargs)
            else:
                plotter = btplot.Plot(**kwargs)

        figs = []
        for stratlist in self.runstrats:
            for si, strat in enumerate(stratlist):
                rfig = plotter.plot(strat, figid=si * 100,
                                    numfigs=numfigs, iplot=iplot,
                                    start=start, end=end, use=use)
                figs.append(rfig)
            # plotter.show()

        return figs