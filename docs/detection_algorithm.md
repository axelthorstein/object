### Circle Detection

#### Simple

I think we could effectively _cheat_ with our circle detection by leveraging our assumptions about the incoming photo. We can assume that the user will at least moderately align the circle on the item with the circle overlay on the web page. If this is the case and we have a perfect alignment then we could crop the image client side to be just larger than the circle, and estimate the colours from the from an arbitrary location in the overlay, and the center point from the overlay. This way we could potentially do all the calculations client side and avoid network overhead. If this is the case we would have an extremely small compute time. 

Realistically the user will not exactly align the overlay with the objects circle. In this case we can still use some assumptions to limit the computation time. Again we can assume the the overlay is relatively aligned with the object circle in which case we can crop the image to slightly larger than the overlay and minimize our matrix size. Once we have a relatively minimal image matrix server side we can assume that the center point of the overlay is inside the objects circle. This would assume the the overlay and the onject circle are at least 50% aligned, which if this assumption is false I think it's reasonable to request realignment from the user. If we are able to appropriately obtain a pixel within the objects circle then we can naively choose any direction to walk and for each pixel determine if there is a colour change. As soon as we change to a distinctly different colour we can assume that we are in the circles ring. At this point we continue walking until we reach the original colour affectively determining the dimensions of our circle. At this point we can use the objects center pixel and a pixel from the circles ring to determine the two colours and create the checkout URL.

A simple error check for this could be taking the center of the ring and confirming that the colour matches the pixel when you transform the location clockwise around the circle.

Example:

```
r, r, r, r, r, r, r, r, r, r
r, r, r, b, b, b, r, r, r, r
r, r, b, b, b, b, b, r, r, r
r, b, b, r, r, r, b, b, r, r
r, b, b, r, r, r ,b, b, r, r
r, b, b, r, r, r, b, b, r, r
r, r, b, b, b, b, b, r, r, r
r, r, r, b, b, b, r, r, r, r
r, r, r, r, r, r, r, r, r, r
r, r, r, r, r, r, r, r, r, r

r: red pixel
b: blue pixel
```

Here we can assume that the image has been cropped by the overlay so that it is not exactly aligned with the object circle. If we use the proposed algorithm to obtain one of the circle pixels (because the matrix has even x, y lengths then there are four potential center pixels) at one of the following locations: (5, 5), (5, 6), (6, 5), (6, 6). Each of these pixels are indeed of the center colour and if we were to choose any of these and walk in any direction we would obtain our second (and ring) colour. Then we would continue until we reached the original colour red, which would be the case in any direction. As an example let us choose the pixel at the coordinates (6, 6) and we walk upwards. We would obtain the array [r, r, r, b, b, r]. With this we can determine that the ring diameter is 2, the colour of the ring is blue, and the center colour is red. With this information we can generate the checkout URL. 

If we wished to error checkout our circle we could take the distance in the array from the center point we chose to find the coordinates for the ring: (6, 6 - 3) -> (6, 3). We should also determine the diameter of the circle so we walk down from the center point and find outside the circle to be 3 pixels down. This way we know 2 things: first that the diameter of the circle is 7, and second that we are in fact not at the center pixel of the circle because we had to walk three up and one down. We then move our center point to (6, 5). Knowing this we can also check our x center point. So we choose an arbitrary x direction and walk. If we choose left and realize we need to walk three to the left, knowing that our inner circle diameter is 3 then we know the center point is at (5, 5). With this we can go back to determining the circle by adding half our inner circle diameter plus half of our ring diamter minus the center point to find the top mid center of the the ring which is (5, round_down(1.5 + 1) - 5) -> (5, 3). We can then determine that the location of the sides and bottom of the ring will be the same fraction of reversed signs:

```
top: (5, round_down(1.5 + 1) - 5) -> (5, 3)
left: (round_down(1.5 + 1) - 5, 5) -> (5, 3)
right: (round_down(1.5 + 1) + 5, 5) -> (5, 3)
bottom: (5, round_down(1.5 + 1) + 5) -> (5, 3)
```

So we are left with an array of [b, b, b, b]. If any of these values were not blue we would invalidate the circles and begin the process again with a new image, or escalate to a more intensive algorithm. 


#### Sampling

Another very quick test that we could do, potentially before our simple analysis, is to sample to cropped image space for expected results. If know that our overlay will be a specific ratio inside our cropped space we could take pixels from the corners, sides, top, inside the overlay, and the center and determine if they match our assumptions. Using our previous example this would look like:

```
# corners
top_left_corner = [1, 1]
bottom_left_corner = [1, 8]
top_right_corner = [8, 1]
bottom_right_corner = [8, 8]

# top, bottom, and sides
top = [1, 5]
bottom = [5, 8]
left = [5, 1]
right = [8, 5]

# center
center_point = [5, 5]
```

From these points we expect that the corners will be red, the sides, top and bottom will be blue, and the center will be red. In reality we can see that all of our assumptions are correct except for the bottom and right are red aswell. This means that our circle is not exactly alighed with our overlay. From this we can escalate to our simple method of detection, but using the previous information we can begin walking to the right and down. If we identify that the ring is in both of these directions we can assume we have found the circle and return the colors.

For the sampling we could also use a median group sample to account for pixel color variability.

# Overlay Assumption

We can increase our validations by making some assumptions about the overlay. If we know that the image will be cropped to a specific ratio and the overlay is in the exact same location on every crop, then as we use our simple detection method we can we can use this assumption to validate on the fly. So for the first walk to the right: We assume that the center point is the center of the crop and walk right from there, and we know exactly where the overlay inner edge starts, so if we reach the circles inner edge before the pixel when the overlay starts we know that either the circle is offset to the left or the circle is smaller than the overlay. We can decide which of these is true by knowing if the overlay width is larger than the circle width then the latter is true, if they are approximately equal then it's the former. 

Let's say then that we know it's offset by 5 pixels, we could then decrement our center x coordinate when we walk left. Then if the circle matches with overlay we know our assumption was right. There could be the case that the right side appears smaller in the photo becasue the fabic is angled, but if that is the case checking the left side would correct for that. If this process is repeated for all directions, continually correcting for offsets, we can be fairly confident in our assumption.