#!/bin/sh


# ufonormalizer ../sources/1-drawing/*.ufo

rm -rf ../build
rm -rf ../fonts/ttf/
mkdir ../build
mkdir ../fonts/ttf/
cd ../build
cp -r ../sources/1-drawing/*.ufo ./

fontmake --ufo-paths *.ufo --output ttf --autohint
mv ./autohinted/master_ttf/* ../fonts/ttf/

rm -rf master_otf
rm -rf master_ttf
rm -rf ./*.ufo
cd ../
rm -rf ./build
