import os
import rasterio

RASTER_FILES = [
    "assets/visual/visual.jp2",
    "assets/bands/B04.jp2",
    "assets/bands/B08.jp2"
]

REPORT_PATH = "reports/raster_inspection.txt"

with open(REPORT_PATH, "w") as report:
    for raster_path in RASTER_FILES:
        header = f"{'='*50}\nFile: {raster_path}\n"
        print(header, end="")
        report.write(header)

        if not os.path.exists(raster_path):
            msg = "STATUS: File not found. Skipped.\n\n"
            print(msg, end="")
            report.write(msg)
            continue

        try:
            with rasterio.open(raster_path) as src:
                info = (
                    f"Width: {src.width}\n"
                    f"Height: {src.height}\n"
                    f"Bands: {src.count}\n"
                    f"CRS: {src.crs}\n"
                    f"Bounds: {src.bounds}\n\n"
                )
                print(info, end="")
                report.write(info)
        except Exception as e:
            error_msg = f"ERROR: Cannot read raster: {e}\n\n"
            print(error_msg, end="")
            report.write(error_msg)

print(f"\nReport saved to: {REPORT_PATH}")
