from PIL import Image


def highlight_regions(img_src, regions, img_dest):
    """
    Takes a source image, highlights regions and saves the result to the destination.
    """
    img = Image.open(img_src)
    for region in regions:
        if (region != (0, 0, 0, 0)):
            img_crop = img.crop(region)
            img_crop = img_crop.convert("RGB")
            overlay = Image.new(
                img_crop.mode, img_crop.size, color=(255, 255, 0))
            img_crop = Image.blend(img_crop, overlay, 0.4)
            img.paste(img_crop, region)
    if (img_dest != "NA"):
        img.save(img_dest)


def get_matching_regions(text_map, query):
    """
    Retrieves the regions of an image which match the query.
    """
    query = query.lower()
    full_text = "".join(text_map[0]).lower()
    letter_matches = [False] * len(text_map[0])
    word_matches = list()
    matching_boundaries = list()
    letter_index = 0
    start_index = 0
    
    for i in range(len(text_map[0])):
        next_start = full_text.find(query, i)
        if (next_start == -1):
            break
        else:
            for j in range(len(query)):
                letter_matches[next_start + j] = True

    for i in range(len(text_map[2])):
        match_found = False
        for j in range(len(text_map[2][i])):
            if (letter_matches[letter_index] and not match_found):
                match_found = True
                start_index = letter_index
            if (match_found and not letter_matches[letter_index]):
                word_matches.append((i, start_index, letter_index - 1))
                match_found = False
            letter_index += 1
        if match_found:
            word_matches.append((i, start_index, letter_index - 1))
        letter_index += 1
    
    for match in word_matches:
        matching_boundaries.append((
            text_map[1][match[1]][0],
            text_map[3][match[0]][1],
            text_map[1][match[2]][2],
            text_map[3][match[0]][3]
        ))
    
    return matching_boundaries


def highlight_matches(img_src, text_map, query, img_dest):
    """
    Highlight matches to a query from a source file and save to destintion file.
    """
    matching_regions = get_matching_regions(text_map, query)
    highlight_regions(img_src, matching_regions, img_dest)
    return len(matching_regions)
