import numpy as np
from PIL import Image

class LBP:
    def __init__(self, input, num_processes, output):
        # Convert the image to grayscale
        self.image = Image.open(input).convert("L")
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.patterns = []
        self.num_processes = num_processes
        self.output = output

    def execute(self):
        self._process()
        if self.output:
            self._output()

    def _process(self):
        pixels = list(self.image.getdata())
        pixels = [pixels[i * self.width:(i + 1) * self.width] for i in range(self.height)]

        # Calculate LBP for each non-edge pixel
        for i in range(1, self.height - 1):
            # Cache only the rows we need (within the neighborhood)
            previous_row = pixels[i - 1]
            current_row = pixels[i]
            next_row = pixels[i + 1]

            for j in range(1, self.width - 1):
                # Compare this pixel to its neighbors, starting at the top-left pixel and moving
                # clockwise, and use bit operations to efficiently update the feature vector
                pixel = current_row[j]
                pattern = 0
                # x << y, retorna "x" com os seus bits movidos "y" casas à esquerda, adicionando zeros aos bits "novos" da direita
                pattern = pattern | (1 << 0) if pixel < previous_row[j-1] else pattern 
                pattern = pattern | (1 << 1) if pixel < previous_row[j] else pattern
                pattern = pattern | (1 << 2) if pixel < previous_row[j+1] else pattern
                pattern = pattern | (1 << 3) if pixel < current_row[j+1] else pattern
                pattern = pattern | (1 << 4) if pixel < next_row[j+1] else pattern
                pattern = pattern | (1 << 5) if pixel < next_row[j] else pattern
                pattern = pattern | (1 << 6) if pixel < next_row[j-1] else pattern
                pattern = pattern | (1 << 7) if pixel < current_row[j-1] else pattern
                self.patterns.append(pattern)

    def _output(self):
        # Write the result to an image file
        result_image = Image.new(self.image.mode, (self.width - 2, self.height - 2))
        result_image.putdata(self.patterns)
        result_image.save("output.png")
