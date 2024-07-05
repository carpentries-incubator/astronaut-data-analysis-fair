## Astronaut data analyses code (FAIR)

This repository contains a helper software project (located in 
the [spacewalks](./spacewalks) subfolder of this repository) with the final, improved and tested code version of the 
[example software project software project](https://github.com/carpentries-incubator/astronaut-data-analysis-not-so-good) used for 
teaching the [FAIR research software course](https://github.com/carpentries-incubator/fair-research-software).

This is the state of the software project the course aims to finish with, 
containing various improvements made on the ["not so good" software project](https://github.com/carpentries-incubator/astronaut-data-analysis-not-so-good) 
the course starts with.

The code analyses the [NASA data on spacewalks](README.md#data) (see details on the data below) by looking at the time astronauts spent in space, crew sizes and the country space missions originated from.
### Authors

The main contributors to this repository are:

- [Sarah Jaffa](https://github.com/sjaffa)
- [Kamilla Kopec-Harding](https://github.com/kkh451)
- [Aleksandra Nenadic](https://github.com/anenadic)


### License

Please see the file [LICENSE](./LICENSE) file for further information about how the content is licensed.

### Acknowledgements

#### Data

The data used on in this project was obtained from NASA as follows.

Data source: https://data.nasa.gov/Raw-Data/Extra-vehicular-Activity-EVA-US-and-Russia/9kcy-zwvn/about_data.

Either export data from the above page using the `Export` button or download in JSON format from command line as: 

`curl https://data.nasa.gov/resource/eva.json --output eva-data.json`

**Note: the original data has been modified for the purposes of this tutorial by inserting a semicolon separator after each name in the `crew` field.**


#### HIFIS 
The idea for this repository has been borrowed from the ["Astronaut analysis" workshop material](https://gitlab.com/hifis/hifis-workshops/make-your-code-ready-for-publication/astronaut-analysis) 
by [Helmholtz Federated IT Services (HIFIS)](https://gitlab.com/hifis).

#### Software Sustainability Institute and UKRN

This work has been supported by the [UK's Software Sustainability Institute](https://software.ac.uk) via the [EPSRC, BBSRC, ESRC, NERC, AHRC, STFC and MRC grant EP/S021779/1](https://gow.epsrc.ukri.org/NGBOViewGrant.aspx?GrantRef=EP/S021779/1)
and [UK Reproducibility Network (UKRN)](https://www.ukrn.org/).

