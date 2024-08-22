import datetime
import time

from matplotlib.colors import ListedColormap, BoundaryNorm
from toolbox.cartopy_tools_OLD import \
    common_features  # <-- This is from https://github.com/blaylockbk/Carpenter_Workshop
import matplotlib.pyplot as plt
from goes2go import GOES
from goes2go.tools import abi_crs

G = GOES(product="ABI-L2-ACHAC", domain="C")
ds = G.nearesttime(datetime.datetime.utcnow().strftime("%y-%b-%d"))
print(ds)
crs, x, y = abi_crs(ds, "HT")

ax = (
    common_features("50m", crs=crs, figsize=[10, 8], dark=True)
)

print(ds.HT)
# Definir los colores (Rojo para "High", Verde para "Mid", Azul para "Low", Negro para "Clear")
colors = ['black', 'blue', 'skyblue', 'green', 'red']

# Crear un ListedColormap
cmap = ListedColormap(colors)

# Definir los límites para las categorías
bounds = [0, 1, 2, 3, 4]

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
ax.set_title(f"{ds.t.dt.strftime('%H:%M UTC %d %b %Y')}")
# Mostrar la figura
fig1 = plt.gcf()
plt.draw()
plt.savefig(f"{time.time()}.jpg", dpi=600)
plt.show()

