boundary 
========

system and services that checks geometry intersections and overlaps

build:
  1. install python, zc.buildout ("zc.buildout==1.5.2") and git
  1. git clone https://github.com/OpenTransitTools/boundary.git
  1. cd boundary
  1. buildout

run:
  1. rm nohup.out; nohup bin/pserve config/development.ini --reload &
  1. http://localhost:45454/stop?stop_id=2&full

test:
  1. run the server (see above)
  1. bin/test
