VBS Print
=========


Publish new version
-------------------

    make package VERSION=master
    scp vbsprint.zip pkg@pkg:www/qgis/vbs/
    ssh pkg@pkg qgis-plugin-repo-scan http://pkg.sourcepole.ch/qgis /home/pkg/www/qgis
