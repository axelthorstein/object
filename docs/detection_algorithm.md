## Circle Detection

The detection algorithm has evolved significantly since I first started developing it and I believe it now stands at a place that will be sufficient for a minimally viable product.

#### Nomenclature:

- **product code:** The character sequence that uniquely identify a product. These are stored in a mapping of product codes to product names.
- **sequence:** The sequence of either brightness values or RGB codes of image pixels (we translate primary colors to simpler codes for fixed length sequences).
- **coordinate map:** The function for generating a sequence of coordinate positions based on a center point and a radius.


### Core Functionality

Taking what I've learned from previous iterations I realized that the quickest approximation (so far) for detecting a sequence from an image is by taking a coordinate map and applying it to various likely locations on the image. If we use our assumptions about where the symbol is most likely to lie within an image we can limit the number of locations that we need to sample. At the present moment I have it set to sample from the center point of the image and 4 directions (left, right, up, down) that are 20% translations in any direction. At each of these translated center points I recalculate the coordinate map with a radius of 75% of the image, then 10% increased and decreased (85% and 65% respectively). This amounts to 15 (5 center points * 3 radii) coordinate maps applied to the image. Given that this step isn't very computationally expensive we can repeat it many times to give us a greater certainty that we've found the circle. And if the circle is found in the first iteration then the search stops and the sequence is returned. That way we can account for the worst case, but hope for the best. Ideally if we preprocess the image properly and enforce strict assumptions from the client side we should see a relatively high level of success.

Additionally, I have added a "fuzzy matching" for the sequences so that if a coordinate map covers 90% of the elements then we can still potentially correctly identify the product code. This is intended to account for image noise, motion blur, brightness variance, etc. from real world examples. The _issue_ with fuzzy matching the product sequences is that the implementation that I have at the moment is slow. It has become the greatest bottleneck behind image filtering with the RAG Merge filter. I don't have insight into the actual implementation because I'm using a library, but I know it is at the least O(n<sup>2</sup>) and likely worse. I want to focus first on correctly identifying the sequences bands, and then I'll focus on speed.

The beauty about separating out the logic for the coordinate maps is that we can completely isolate a symbol per coordinate map and then we can easily translate and transform it before applying it to an image to identify sequences. And because the sequences are based on either RGB color values or brightness values, then we have a lot of flexibility of what symbol we use.


### Assumptions

A lot of the algorithm relies on some assumptions about the image:

- The image must be a certain size with the symbol as close to the center as possible.
- It must be taken from a straight angle so the symbol isn't skewed.
- There shouldn't too much noise or varying brightnesses
- It should be large enough that it takes up about 75% of the frame. If these conditions are approximately met then the algorithm should be able to identify the sequence on the first iteration and very quickly return the product code.


### Image Filtering

In reality, we will have noise in images. The incoming images will be taken by users in a variety of locations and the symbol will be on fabric so the image could be skewed, too dark, too light, have undefined noise, too close, too far, etc. In order to counteract the presence of noise we can filter the images before we begin processing. We have simple merge and sharpening that we do to every image which help reduce a minimal amount of noise, however I have implemented RAG Merge filtering which can greatly reduce excess noise from an image and give us a really clean image to work with. The issue is that it's resource intensive. We could potentially run this on an external GPU, or test running it on client machines, but if we could preprocess every image with this quickly it would greatly increase our success rate.
