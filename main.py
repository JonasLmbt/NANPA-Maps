from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box


def _pad_bounds(bounds: tuple[float, float, float, float], pad_ratio: float) -> tuple[float, float, float, float]:
    minx, miny, maxx, maxy = bounds
    dx = maxx - minx
    dy = maxy - miny
    if dx == 0:
        dx = 1.0
    if dy == 0:
        dy = 1.0
    padx = dx * pad_ratio
    pady = dy * pad_ratio
    return (minx - padx, miny - pady, maxx + padx, maxy + pady)

def _make_square_bounds(bounds: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    minx, miny, maxx, maxy = bounds

    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2

    width = maxx - minx
    height = maxy - miny
    half_size = max(width, height) / 2

    return (
        cx - half_size,
        cy - half_size,
        cx + half_size,
        cy + half_size,
    )

def render_area_code_map_zoomed(
    boundaries_path: str,
    area_code: str,
    out_path: str,
    *,
    code_field: str = "NPA",
    figsize: tuple[int, int] = (12, 8),
    pad_ratio: float = 0.25,
    background_mode: str = "local",  # "local" or "all"
    crs_epsg: int = 3857,
    label_in_polygon: bool = True,
    label_fontsize: int = 26,
) -> None:
    gdf = gpd.read_file(boundaries_path)

    if code_field not in gdf.columns:
        raise ValueError(f"Column '{code_field}' not found. Available columns: {list(gdf.columns)}")

    gdf[code_field] = gdf[code_field].astype(str).str.strip()
    area_code = str(area_code).strip()

    selected = gdf[gdf[code_field] == area_code]
    if selected.empty:
        raise ValueError(f"Area code '{area_code}' not found in column '{code_field}'.")

    gdf = gdf.to_crs(epsg=crs_epsg)
    selected = selected.to_crs(epsg=crs_epsg)

    zoom_bounds = _pad_bounds(selected.total_bounds, pad_ratio=pad_ratio)
    zoom_bounds = _make_square_bounds(zoom_bounds)
    zoom_geom = box(*zoom_bounds)

    # Zoom-dependent font size
    zoom_width = zoom_bounds[2] - zoom_bounds[0]
    zoom_height = zoom_bounds[3] - zoom_bounds[1]
    zoom_scale = max(zoom_width, zoom_height)
    print(f"Zoom scale: {zoom_scale}")

    # Tunable constants
    fontsize = 3_000_000 / zoom_scale * 6
    fontsize = max(10, min(22, fontsize))
    print(f"Determined fontsize: {fontsize}")

    if background_mode == "local":
        background = gdf[gdf.intersects(zoom_geom)]
    elif background_mode == "all":
        background = gdf
    else:
        raise ValueError("background_mode must be 'local' or 'all'.")

    fig, ax = plt.subplots(figsize=figsize)

    background.plot(ax=ax, color="#cac3c3", edgecolor="#272626", linewidth=0.5)
    selected.plot(ax=ax, color="#ffcccc", edgecolor="#aa0000", linewidth=1.2)

    ax.set_xlim(zoom_bounds[0], zoom_bounds[2])
    ax.set_ylim(zoom_bounds[1], zoom_bounds[3])

    ax.set_axis_off()

    # Remove title and draw label inside the selected area
    if label_in_polygon:
        # One label position for the union of all selected polygons
        label_point = selected.unary_union.representative_point()
        ax.text(
            label_point.x,
            label_point.y,
            area_code,
            ha="center",
            va="center",
            fontsize = fontsize,        
            fontweight="normal",  
            color="#1a1a1a",
            zorder=10,
        )


    out_path = str(out_path)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=220, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


if __name__ == "__main__":
    boundaries_path = "area-codes.geojson"  # keep the filename consistent
    area_code=[304, 318, 319, 337, 515, 520, 563, 601, 641, 662]
    gdf = gpd.read_file(boundaries_path)

    for a in area_code:
        a = str(a)
        render_area_code_map_zoomed(
            boundaries_path=boundaries_path,
            area_code=a,
            out_path=f"out/{a}.png",
            code_field="NPA",
            pad_ratio=3,
            background_mode="local",
        )

        render_area_code_map_zoomed(
            boundaries_path=boundaries_path,
            area_code=a,
            out_path=f"out/{a}_zoomed.png",
            code_field="NPA",
            pad_ratio=1,
            background_mode="local",
        )
