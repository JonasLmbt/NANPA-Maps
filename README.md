# NANPA Maps (Area Code Map Renderer)

Small Python script that renders PNG maps for North American Numbering Plan (NANP) area codes from a GeoJSON boundary file.

## What it does

- Reads a polygon GeoJSON (default: `area-codes.geojson`)
- Selects a single area code by attribute (default field: `NPA`)
- Renders two images per code:
  - a "wide" view (more padding)
  - a "zoomed" view (less padding)
- Writes results to `out/`

## Requirements

- Python 3.10+ (recommended)
- `geopandas`
- `shapely`
- `matplotlib`

Example install:

```bash
python -m pip install geopandas shapely matplotlib
```

## Usage

Run the script:

```bash
python main.py
```

Adjust the `area_code` list and other parameters in `main.py` to your needs.

## Notes

- GitHub has a hard file size limit of 100 MB. `area-codes.geojson` in this repo is ~97 MB, so it's close to the limit.
- Ensure you have the rights to redistribute the GeoJSON data file (`area-codes.geojson`) if you publish this repository.
