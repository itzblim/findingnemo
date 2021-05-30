from PIL import Image


def highlight_regions(img_src, regions, img_dest):
    """
    Takes a source image, highlights regions and saves the result to the destination.
    """
    img = Image.open(img_src)
    for region in regions:
        if (region != (0, 0, 0, 0)):
            img_crop = img.crop(region)
            overlay = Image.new(
                img_crop.mode, img_crop.size, color=(255, 255, 0))
            img_crop = Image.blend(img_crop, overlay, 0.4)
            img.paste(img_crop, region)
    if (img_dest != "NA"):
        img.save(img_dest)
    return img


def get_matching_regions(text_map, query):
    """
    Retrieves the regions of an image which match the query.
    """
    query = query.lower()
    full_text = "".join(text_map[0]).lower()
    matches = [False] * len(text_map[0])

    for i in range(len(text_map[0])):
        next_start = full_text.find(query, i)
        if (next_start == -1):
            break
        else:
            for j in range(len(query)):
                matches[next_start + j] = True

    matching_regions = list()
    for i in range(len(matches)):
        if matches[i]:
            matching_regions.append(text_map[1][i])

    return matching_regions


def highlight_matches(img_src, text_map, query, img_dest):
    """
    Highlight matches to a query from a source file and save to destintion file.
    """
    highlight_regions(img_src, get_matching_regions(text_map, query), img_dest)
