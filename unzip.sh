#!/bin/bash

function traverse_dir {
  local dir=$1
  local sub_dir
  local file
  for file in "$dir"/*
  do
    if [[ -d "$file" ]]
    then
      traverse_dir "$file"
    elif [[ "$file" == *.zip || "$file" == *.7z || "$file" == *.rar || "$file" == *.zipx ]]
    then
      filename=$(basename "$file" | cut -f 1 -d '.')
      mkdir -p "$dir/$filename"
      if [[ "$file" == *.zip ]]
      then
        unzip -o -qO UTF-8 "$file" -d "$dir/$filename"
        traverse_dir "$dir/$filename"
      elif [[ "$file" == *.7z ]]
      then
        7z x "$file" -o"$dir/$filename" -y
        traverse_dir "$dir/$filename"
      elif [[ "$file" == *.rar ]]
      then
        unrar x "$file" "$dir/$filename"
        traverse_dir "$dir/$filename"
      elif [[ "$file" == *.zipx ]]
      then
        unzip -o -qO UTF-8 "$file" -d "$dir/$filename"
        traverse_dir "$dir/$filename"
      fi
    fi
  done
}

# 指定要遍历的文件夹
dir="./image"

# 调用递归函数遍历文件夹中的所有文件并解压压缩包
traverse_dir "$dir"
