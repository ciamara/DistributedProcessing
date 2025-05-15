import sys
import time
import cv2
import numpy as np
import multiprocessing as mp
from PIL import Image


# slicing image into *parts* horizontal lines
def scatter(image, parts):
    print("Scattering image...")
    slices = np.array_split(image, parts, axis=0)
    return slices

# sticking slices back together
def gather(slices):
    print("Gathering image...")
    return np.vstack(slices)

# convert single slice to negative
def convert_slice(slice):
    neg = 255 - slice
    return neg

# multiprocessing
def convert(image, parts):
    print("Converting slices into negatives...")

    slices = scatter(image, parts)

    with mp.Pool(parts) as pool:
        neg = pool.map(convert_slice, slices)

    result = gather(neg)

    return result

def main():
    
    if len(sys.argv) < 2:
        print("Usage: python scatterGather.py <number_of_processes>")
        return

    parts = int(sys.argv[1])

    image = Image.open('mystical.jpg').convert("RGB")
    imageArray = np.array(image)
    
    start = time.time()

    negative = convert(imageArray, parts)

    end = time.time()
    print(f"Execution time: {end - start:.4f} seconds")

    result = Image.fromarray(negative.astype(np.uint8))

    print("Saving image...")
    result.save('neg.jpg')

    sys.exit(0)

if __name__ == "__main__":
    main()
