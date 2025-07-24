#!/bin/bash

# 指定要遍历的文件夹
dir="./image"

# 遍历文件夹中的所有子文件夹
for subdir in "$dir"/*/
do
  # 提取子文件夹名称
  subdir=$(basename "$subdir")

  # 指定输出文件名
  gif_output="$dir/$subdir/$subdir.gif"
  apng_output="$dir/$subdir/$subdir.png"
  for file in "$dir/$subdir"/*
  do
    # 提取文件名和后缀名
    filename=$(basename "$file")
    extension="${filename##*.}"
  done

  # 使用 FFmpeg 制作 GIF
  ffmpeg -y -f image2 -framerate 10  -i "$dir/$subdir/000%03d.$extension" -c:v gif "$gif_output"

  # 使用 FFmpeg 制作 APNG
  ffmpeg -y -f image2 -framerate 10  -i "$dir/$subdir/000%03d.$extension" -f apng -plays 0 "$apng_output"
done
