# Puppy Scientific Computing Talk: Clustering ZCTA5

The notebook contains the one-off analysis, which saves the model details.
The model details are contained in the model folder, so the app
can be run immediately.

## Run locally

Clone repo and then run the following from the project root:

```
$ docker build -f Dockerfile -t puppy_clustering .
$ docker run -v /full/path/to/project/root/:/root/app -p 0.0.0.0:8080:8080 -it puppy_clustering bash
```

Then direct your browser to http://localhost:8080

## Notes

* Analysis requires R with packages: usdm, archetypes
* Docker

## Some package requirements
* Plotly
* Dash
* rpy2 
