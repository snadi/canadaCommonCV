Avoid the pain of the Common CV

# License

This software is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.

# Introduction

If you are here, you are looking for a relief from the Common CCV user
interface. How much do you think that interface has cost? Don\'t even
think of knowing the answer. It might sink you into depression.

These scripts will allow you to avoid the CCV user interface and
instead, concentrate on just uploading XML files.

# Restrictions

-   These scripts are specifically designed to target Computer Science.
-   It only handles conferences and journals
-   They run under Linux, but might work under OS X
-   They only handle cases I have seen (for example, it does not include
    all the countries in the world (why does the CCV care to verify
    them?)

# Requirements

-   Linux or MacOS
-   pdftolatex (converts ccv in pdf to text, only needed if you want to
    create a bibtex bibliography that matches your ccv)
-   ruby
-   perl
-   latex
-   python 3.x
-   make

# How to use

- Create a python virutal environment
  - python -m venv .venv
  - source .venv/bin/activate
  - pip install -r requirements 
- Create your input bib file in the `input` directory (`<bibfilename>`). 
- If you want to automatically highlight hqp names, then update your HQP names in `scripts/hqp.py`
- Run `make INPUT_BIB=<bibfilename>` 
- The above command will generate the following files in the `output` directory:
    -   journals.xml and confs.xml
    -   journals.bib and confs.bib


# Uploading the XML files

-   Login to the CCV
-   I **strongly recommend you backup your current CCV by first
    downloading it in XML**. See Warranty above.
-   Go to the import tab.
-   Specify that you want to import XML.
-   You will be asked for a file to upload.
-   Upload
-   At this point it will verify your XML. If it is all good, you will
    get no errors. If you get errors, well, they are very hard to debug
    (thank the ccv). I recommend you split your bibliography in smaller
    chunks and test each.
-   Now that it has verified it will ask you to indicate what section of
    the CCV you want to import it into.
    -   Select journals or conferences appropriately
-   Verify the data was read by browsing the current ccv.

# Intermediate Format Used

The scripts automatically convert the input bib file to various intermediate formats before creating the final XML format CCV accepts. First, the bib files are converted to a json format, which is then converted to Daniel German's input txt format below. If you would like to see these intermediate files, you can remove the `rmtmpfiles` dependency from the `default` target in the Makefile.

See the directory [*sample*]{.spurious-link target="sample"} for
examples of these files.

Each file is a list of publications, in text file. The referenceID must
be unique (somebody willing to write a patch to not-require it?)

This is an example of a Journal:

    recordId=5f84ac4e98bc482dba87b56f001ea640
    Title=Management of community contributions
    Journal=Empirical Software Engineering
    Volume=20
    Issue=1
    PageRange=252-289
    PublishingStatus=Published
    Date=2015/2
    Publisher=Springer
    URL=http://link.springer.com/article/10.1007%2Fs10664-013-9284-6
    Refereed=Yes
    OpenAccess=No
    Authors=Nicolas Bettenburg, Ahmed E. Hassan, Bram Adams, Daniel M. German
    dmgKey=dmg2015nickESE

And this is an example of a conference:

    recordId=5f84ac4e98bc48200087b56f001ea640
    Type=Paper
    Title=Open Source-Style Collaborative Development Practices in Commercial Projects Using GitHub
    Conference=37th International Conference on Software Engineering (ICSE'15)
    Country=Italy
    City=Florence
    Date=2015/5
    DateConf=2015-05-16
    PublishedIn=Proc. 37th International Conference on Software Engineering, ICSE '15
    PublishingStatus=Published
    Refereed=Yes
    Authors=<b>E. Kalliamvakou*</b>, D. Damian, K. Blincoe, L. Singer, Daniel M. German
    Publisher=Springer
    Note=Acceptance rate 18% (84 out of 276 research papers).
    DOI=http://dx.doi.org/10.1109/ICSE.2015.74
    dmgKey=dmg2015icseGithub

One line per field, and separate records with an empty line. Some HTML
is allowed in the CCV, but not everywhere.




# Create a bibliography for latex that can reference your CCV

In the directory latexCrossRef you will find a way to create an Latex
bibliography input file that you can use to reference your CCV using standard bibtex
citations.

For example, these are some of my publications in the ccv:

[]{.image .placeholder original-image-src="./images/j.png"
original-image-title=""}

[]{.image .placeholder original-image-src="./sample/c.png"
original-image-title=""}

And this is how I refer to them in the proposal:

``` LaTeX
...
difficulties of tracing contributions in email and version control systems \cite{dmg2015contMining,dmg2014esemMailCommits}.
We have empirically observed how distributions perform integration~\cite{dmg2014eseDebianInt}, and how software
ecosystems manage their contributions and releases~\cite{dmg2015emseCommuContrib,dmg2013csmrR}
We identified code reviews as a crucial tool for quality control in FOSS projects, investigated the
manner in which they are performed via email, and found them to be as
effective as those in commercial software~\cite{dmg2014tosemReviews,dmg2012ieeeReviews}. We have also explored the
challenges of adopting and upgrading FOSS libraries~\cite{dmg2015icsmeEralib,dmg2014vissoftLib}.
...
```

and this is how it appears:

[]{.image .placeholder original-image-src="./images/la.png"
original-image-title=""}

## How it works

-   The **input** file is your CCV (name it ccv-nserc.pdf) and the
    bib file that contains all your publications (the same one you used to generate your CCV above)
-   Place your downloaded ccv-nserc.pdf file in `input/` -- or change the location but update the Makefile accordingly
-   The important file to generate is `ccv_references.aux``
-  Run the following. Note that the input bib file is just the name of the bib file found in `input/`
```
cd latexCrossRef
make INPUT_BIB=<your input bib file>
```

## Steps

-   download a recent version of the CCV (pdf) since any updates to your CCV will change the references numbers
-   run make
-   if no errors, verify that the generated `ccvReferences.txt` in this directory matches the order of your CCV. Otherwise, something is wrong

## How to use

Copy the generated aux file to your main latex project directory. In your main tex file:

```LaTeX
\usepackage{xcite}
\externalcitedocument{ccv_references}
```
then you can cite refernces from your own work as usual. Note that these cited references will appear as `[C1, J3]` etc. in the text but WILL NOT appear again in the reference list of your proposal (which is the desired end result).

