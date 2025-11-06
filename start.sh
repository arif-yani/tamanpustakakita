#!/bin/bash

PWD=/opt/odoo17
source $PWD/venv17/bin/activate

odoo -c odoo17.conf

deactivate
