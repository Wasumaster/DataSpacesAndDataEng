import os
import rasterio
import numpy as np

RASTER_FILES = {
    "B04": "assets/bands/B04.jp2",
    "B08": "assets/bands/B08.jp2"
}

REPORT_PATH = "reports/spectral_statistics.txt"

with open(REPORT_PATH, "w") as report:
    for name, path in RASTER_FILES.items():
        header = f"{'='*50}\nBand: {name} | File: {path}\n"
        print(header, end="")
        report.write(header)

        if not os.path.exists(path):
            msg = "STATUS: File not found. Skipped.\n\n"
            print(msg, end="")
            report.write(msg)
            continue

        try:
            with rasterio.open(path) as src:
                band = src.read(1)
                
                b_min = np.min(band)
                b_max = np.max(band)
                b_mean = np.mean(band)
                b_std = np.std(band)

                stats = (
                    f"MIN: {b_min}\n"
                    f"MAX: {b_max}\n"
                    f"MEAN: {b_mean:.2f}\n"
                    f"STD: {b_std:.2f}\n\n"
                )
                print(stats, end="")
                report.write(stats)
        except Exception as e:
            err = f"ERROR: {e}\n\n"
            print(err, end="")
            report.write(err)

print(f"\nReport saved to: {REPORT_PATH}")
