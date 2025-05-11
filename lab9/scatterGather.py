import os
import sys
import time
import cv2
import numpy as np
import pickle
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# slicing image into *parts* horizontal lines
def scatter(image, parts):
    print("Slicing the image into horizontal parts")
    h, w, _ = image.shape
    step = h // parts
    return [image[i*step:(i+1)*step if i != parts-1 else h, :] for i in range(parts)]

# sticking slices back together
def gather(slices):
    print("Sticking the converted parts back together")
    return np.vstack(slices)

# processes & converting to negative
def fork_processes(slices):

    print("Converting slices to negative simultaneusly")

    children = []
    pipes = []

    for i, sl in enumerate(slices):
        r, w = os.pipe()
        pid = os.fork()
        if pid == 0:
            # child process (converting to negative)
            os.close(r) 
            sl_neg = 255 - sl
            data = pickle.dumps(sl_neg)
            os.write(w, data)
            os.close(w)
            os._exit(0)
        else:
            # parent process
            os.close(w)
            children.append(pid)
            pipes.append(r)

    # converted slices from children
    results = []
    for r in pipes:
        data = b''
        while True:
            chunk = os.read(r, 4096)
            if not chunk:
                break
            data += chunk
        results.append(pickle.loads(data))
        os.close(r)

    # wait for all children to finish
    for pid in children:
        os.waitpid(pid, 0)

    return results

def main():
    
    if len(sys.argv) < 2:
        print("Usage: python3 program.py <number_of_processes>")
        return

    parts = int(sys.argv[1])
    image = cv2.imread('BIGobszar.jpeg')
    cv2.imshow("original", image)

    start = time.time()

    slices = scatter(image, parts)
    converted = fork_processes(slices)
    full = gather(converted)

    end = time.time()
    print(f"Execution time: {end - start:.4f} seconds")

    cv2.imshow("Negative Combined", full)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    sys.exit(0)

if __name__ == "__main__":
    main()
