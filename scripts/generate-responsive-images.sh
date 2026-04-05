#!/bin/bash

# Navigate to project directory
cd "$(dirname "$0")/.."

# Create output directory
output_dir="jpg/responsive"
mkdir -p "${output_dir}"

# Define image widths
sizes=(320 480 640 768 960 1024 1366 2048 2732)

# Source images
source_images=(
    "jpg/2025-ASIS+T-Poster.jpg"
    "jpg/2025-ASIS+T-1st-Place-Prize.jpg"
)

# Generate responsive images for each source
for source_image in "${source_images[@]}"; do
    # Extract base name without extension and directory
    base_name=$(basename "${source_image}" .jpg)

    echo "Processing ${base_name}..."

    for size in "${sizes[@]}"; do
        echo "  Generating ${size}w variant..."

        convert "${source_image}" \
            -resize "${size}x${size}>" \
            -sampling-factor 4:2:0 \
            -strip \
            -quality 85 \
            -interlace JPEG \
            -colorspace sRGB \
            "${output_dir}/${base_name}-${size}w.jpg"
    done
done

echo "All responsive images generated in ${output_dir}/"
echo -e "\nGenerated files:"
ls -lh "${output_dir}/"
