# region VisIR2D


p_VisIR2D = figure()


@gen.coroutine
def callback_update_vis_ir_fig(delay, visible):
    mplt = mcfg.data_matrix
    cmap = cm.get_cmap("jet")  # choose any matplotlib colormap here
    num_slabs = 10  # number of color steps
    jet_10 = [colors.rgb2hex(m) for m in cmap(
        np.arange(0, cmap.N, cmap.N/(num_slabs-1)))]
    vmin = 0
    vmax = 1550
    N = 200
    x = np.linspace(0, 10, N)
    y = np.linspace(0, 10, N)
    xx, yy = np.meshgrid(x, y)
    d = vmax * (1. + np.sin(xx)*np.cos(yy))

    source = ColumnDataSource(data={'d': [d], 'x': [x], 'y': [y]})
    p_VisIR2D.image(image="d", palette=jet_10, source=source)

    # The following code is for the colorbar:
    pcb = figure(plot_width=80, plot_height=400, x_range=[
                 0, 1], y_range=[0, vmax], min_border_right=10)
    pcb.image(image=[np.linspace(vmin, vmax, 100).reshape(100, 1)], x=[
              0], y=[0], dw=[1], dh=[vmax-vmin], palette=jet_10)
    pcb.xaxis.major_label_text_color = None
    pcb.xaxis.major_tick_line_color = None
    pcb.xaxis.minor_tick_line_color = None
    pcb.yaxis[0].ticker = FixedTicker(
        ticks=np.linspace(vmin, vmax, num_slabs+1))  # 11 ticks
    # this places the colorbar next to the image
    pgrid = gridplot([[p_VisIR2D, pcb]])


callback_update_vis_ir_fig(1, 1)

# endregion
