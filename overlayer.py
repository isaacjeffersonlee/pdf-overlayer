import os
import argparse
from pdf2image import convert_from_path

# For MacOS
# https://macappstore.org/poppler/


def main(in_path: str, title_overlay: str = '', overlays: list[str] = []) -> None:
    if os.path.isdir(in_path):
        if in_path[-1] != "/":
            in_path += "/"  # Make sure directory name is of the form dir/
        files_to_overlay = [in_path + file for file in os.listdir(in_path)]
    elif os.path.isfile(in_path):
        files_to_overlay = [in_path]
    else:
        raise FileNotFoundError(f"The file or directory {in_path} was not found!")

    if not os.path.exists("png_pages"):
        os.mkdir("png_pages")  # Make a temporary directory to do operations in

    for idx, file in enumerate(files_to_overlay):
        print(f"Overlaying file: {file}, {idx+1}/{len(files_to_overlay)}")
        pdf = convert_from_path(file)
        if overlays:
            dim_to_overlay_map = {}
            overlay_idx = 0
            for page in pdf:
                page_dimensions = (page.width, page.height)
                if page_dimensions not in dim_to_overlay_map.keys():
                    dim_to_overlay_map[page_dimensions] = overlays[
                        overlay_idx % len(overlays)
                    ]
                    overlay_idx += 1

        for i in range(len(pdf)):
            # Select the correct overlay for the page dimensions
            img_path = f"png_pages/{i}_unedited.png"
            pdf[i].save(img_path, "PNG")
            if overlays:
                if i == 0 and title_overlay:
                    overlay = title_overlay
                else:
                    page_dimensions = pdf[i].width, pdf[i].height
                    overlay = dim_to_overlay_map[page_dimensions]
                os.system(
                    f"magick composite -gravity center {overlay} png_pages/{i}_unedited.png png_pages/{i}_overlayed.png"
                )

        # Extract only the files name, without extension
        file_name = file.split(".pdf")[0]
        # Combine the overlayed images together back into a single pdf
        os.system(f"convert png_pages/*_overlayed.png {file_name}_overlayed.pdf")
        print("Finished overlaying file")
        print(f"{file} >> {file_name}_overlayed.pdf")
        print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        dest="in_path",
        help="Input pdf file/directory of pdfs to add the overlay to.",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--title-overlay",
        dest="title_overlay",
        help="Overlay to only apply to the first page.",
    )
    parser.add_argument(
        "-o",
        "--overlay",
        nargs="+",
        dest="overlays",
        help="[Optional] Image to overlay over each page of the pdf.",
    )
    args = parser.parse_args()

    main(args.in_path, args.title_overlay, args.overlays)
