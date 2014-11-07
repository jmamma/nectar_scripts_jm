#!/bin/bash

#Justin Mammarella 06/11/2014

#Helper functions called in by other scripts.


getNode() {

        if ! check_admin_credentials; then
            return 1
        fi

}
