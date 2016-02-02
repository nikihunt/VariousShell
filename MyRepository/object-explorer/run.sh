#!/bin/bash
mvn install:install-file -Dfile=object-explorer.jar \
	  -DgroupId=com.google \
	    -DartifactId=memory-measurer \
	      -Dpackaging=jar \
	        -Dversion=1.0-SNAPSHOT \
		  -Dfile=dist/object-explorer.jar \
		    -DgeneratePom=true
