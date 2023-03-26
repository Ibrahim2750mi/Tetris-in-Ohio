import sys

from PIL import Image

if __name__ == '__main__':
    im = Image.open(full_path := sys.argv[1], )
    im_width, im_height = im.size

    # If rectangle, pass decrement to make it square.
    balance_height = int(sys.argv[2])

    # Image needs to be square.
    for i in range(im_width // (im_height + balance_height)):
        new_im = im.crop(((im_height + balance_height) * i, 0, (im_height + balance_height) * (i + 1), im_height))

        file_path = f"{'/'.join((im_path := full_path.split('/'))[:-1])}/{im_path[-1].split('.')[0]}_{str(i)}.png" \
            .replace(str(im_height + balance_height), str(im_height))
        new_im.save(file_path)
