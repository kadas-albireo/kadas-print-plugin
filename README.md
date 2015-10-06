VBS Print
=========


Publish new version
-------------------

    make package VERSION=master
    scp vbsprint.zip builder@builder:www/qgis/vbs/
    ssh builder@builder qgis-plugin-repo-scan http://build.sourcepole.ch/qgis /home/builder/www/qgis
