#!/bin/bash

# Navigate to project directory
cd /media/aw/057f994c-3b81-4968-9a85-8ce3ef78dfbf/GitHub/dh-ai-disclosure

# Create backup of original
cp jpg/2025-ASIS+T-1st-Place-Prize.jpg jpg/2025-ASIS+T-1st-Place-Prize-original.jpg

# Create output directory
output_dir="jpg/responsive"
mkdir -p "${output_dir}"

# Define image widths
sizes=(320 480 640 768 960 1024 1366 2048 2732)

# Source image
source_image="jpg/2025-ASIS+T-1st-Place-Prize.jpg"

# Generate responsive images
for size in "${sizes[@]}"; do
    echo "Generating ${size}w variant..."

    convert "${source_image}" \
        -resize "${size}x${size}>" \
        -sampling-factor 4:2:0 \
        -strip \
        -quality 85 \
        -interlace JPEG \
        -colorspace sRGB \
        "${output_dir}/2025-ASIS+T-1st-Place-Prize-${size}w.jpg"
done

echo "All responsive images generated in ${output_dir}/"
echo -e "\nGenerated files:"
ls -lh "${output_dir}/"
