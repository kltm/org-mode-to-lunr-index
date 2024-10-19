# org-mode-to-solr

Simple python code to convert my org-mode notes to something
searchable, using solr docker images.

This is after an awful long time of trying to get various org-mode
packages to emit something I found usable and either 1) getting
something that would be just as painful to get into solr or 2)
crashing out emacs.

So...doing it the old-fashioned way with some silly python.

## Steps

`python3 bulk-convert.py -v -f ~/notes.org > notes.json`

From https://solr.apache.org/guide/solr/latest/deployment-guide/solr-in-docker.html .
Get a docker image up and create a core for it. Lifecycle:

`docker run -d -p 8983:8983 --name notes_solr solr solr-precreate notes_core`
`docker kill notes_solr`
`docker rm notes_solr`

Load what we have:

`curl 'http://localhost:8983/solr/notes_core/update/json?commit=true' --data-binary @notes.json -H 'Content-type:application/json'`

Go to:

http://localhost:8983/solr/#/notes_core/query

## TODO

TODO

## Notes

Initially seeded with some ChatGPT code, but after working with it
nothing non-trivial remained in any meaningful way. Removing that
note.
