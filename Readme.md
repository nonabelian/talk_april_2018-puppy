# Puppy Scientific Computing Talk April 2018
## Demographic Clustering ZCTA5

(Presentation slides in docs folder.)

It can be very interesting to perform regional clustering of the US based
on census data.  This is done, for example, at
[Patchwork Nation](http://www.patchworknation.org/)
and
[ESRI](https://www.esri.com/data/esri_data), to name a few. There, groups are
clustered based on various attributes, across the US.  I happened to pick a
dataset that involves some sensitive topics, but in principle the analysis can
be applied to anything.

In any event, let's have a look at some clustering!

## Analysis and App

Goal:

* Preprocess and join any relevant data.
* Drop sparse/redundant features.
* Remove outliers for quality clusters.
* Apply [Archetypal Analysis]
(https://en.wikipedia.org/wiki/Archetypal_analysis)
to pull out distinct segments.
* Build web application for navigating the clusters.

The notebook (in the 'notebooks' folder) contains the one-off analysis, which
saves the model details.  The model details are saved in the model folder,
so the app can be run immediately.  The web app should be ready to be deployed
(with possible adjustments for different platforms). Details for running the
web app locally are in the next section. You can find an example screenshot
of the web app in the 'images' directory:

## Run locally

Clone repo and then run the following from the project root:

```
$ docker build -f Dockerfile -t puppy_clustering .
$ docker run -v /full/path/to/project/root/:/root/ -p 0.0.0.0:8080:8080 -it puppy_clustering bash
```
And within the container:
```
# python app.py
```

Then direct your browser to http://localhost:8080

## Notes

* Analysis requires R with packages: usdm, archetypes
* Docker

## Some package requirements
* Plotly
* Dash
* rpy2 
