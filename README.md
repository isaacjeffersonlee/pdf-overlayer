# PDF Overlayer
### Author: Isaac Lee

## Intro
Takes a pdf file/directory of pdf files and an image/list of images
and overlays the image on each page, saving the result as a new pdf.


## Requirements
The only python requirement not in the base python install (os and argparse are requried by
already in the base install of Python), is [pdf2image](https://pypi.org/project/pdf2image/):
```shell
pip install pdf2image
```

## Installation

### Linux
Requires the `imagemagick` and `poppler-utils` packages:
For arch based:
```shell
sudo pacman -S imagemagick poppler
```
For debian based (ubuntu included):
```shell
sudo apt install imagemagick poppler-utils
```

### MacOS
To install imagemagick, the [brew](https://brew.sh/) is recommended:
```shell
brew install imagemagick
```
Also imagemagick depends on the ghostscript fonts:
```shell
brew install ghostscript
```
Then to install the poppler-utils for mac see the instructions [here](https://macappstore.org/poppler/).

### Windows
Delete windows, then install Linux and see above instructions.

### Cloning the repo
Once all of the dependencies have been installed, simply clone the repo and cd into it:
```shell
git clone https://github.com/isaacjeffersonlee/pdf-overlayer
cd pdf-overlayer/
```
For useage see next section...

## Usage
Single file, simple use case, stamp every page of the pdf with the same image:
```shell
python overlayer.py -i input.pdf -o overlay.png
```
Apply an overlay to all pages of all pdfs in a directory:
```shell
python overlayer.py -i pdf_dir/ -o overlay.png
```
Note: make sure the only files in the dir are the pdfs you want to overlay.

Also if your pdf has pages with multiple dimensions, i.e some
pages are landscape and some are portrait, then you can specify
multiple overlays to overlay and they will be applied in
the order that the pages appear. I.e Suppose our pdf pages are as follows:
portrait, portrait, landscape, portrait, landscape, ...
then we would use:
```shell
python overlayer.py -i input.pdf -o portrait_overlay.png landscape_overlay.png
```
and overlayer.py will detect the different resolutions and switch between
overlay images accordingly.  

Often title pages have a different layout, so you can also specify a different
overlay for the first page using the `-t` option:
```shell
python overlayer.py -i input.pdf -o overlay.png -t title_overlay.png
```

Optionally you can also specify no overlay images and this will
have the effect of removing all meta data from the pdf, which
is possibly a desirable effect:
```shell
python overlayer.py -i input.pdf
```
