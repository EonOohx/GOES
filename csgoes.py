import datetime
import time

from matplotlib.colors import ListedColormap, BoundaryNorm
from toolbox.cartopy_tools_OLD import \
    common_features  # <-- This is from https://github.com/blaylockbk/Carpenter_Workshop
import matplotlib.pyplot as plt
from goes2go import GOES
from goes2go.tools import abi_crs

G = GOES(product="ABI-L2-ACHAC", domain="C")

inicio = time.time()
while True:
    if time.time() - inicio > 360:
        try:
            ds = G.latest()
            crs, x, y = abi_crs(ds, "HT")

            ax = (
                common_features("50m", crs=crs, figsize=[10, 8], dark=True)
            )

            # Definir los colores (Rojo para "High", Verde para "Mid", Azul para "Low", Negro para "Clear")
            colors = ['black', 'blue', 'skyblue', 'green', 'red']

            # Crear un ListedColormap
            cmap = ListedColormap(colors)

            # Crear el gráfico de pcolormesh
            c = ax.pcolormesh(x, y, ds.HT, transform=crs, cmap=cmap, vmin=0)

            # Crear la barra de colores utilizando el objeto 'c' generado por pcolormesh
            cbar = plt.colorbar(
                c,
                ax=ax,
                shrink=0.8,
                pad=0.01,
                orientation="horizontal",
                label=f"{ds.HT.long_name}\n({ds.HT.units})"
            )


            # Establecer el título
            name = ds.t.dt.strftime('%H:%M UTC %d %b %Y').item()
            ax.set_title(f"{name}")
            # Mostrar la figura
            fig1 = plt.gcf()
            plt.draw()
            plt.savefig(f"{name}.jpg", dpi=600)
            plt.close()
            inicio = time.time()
        except Exception as e:
            print(e)

