#!/bin/bash

rm -rf build dist rlanutils.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*