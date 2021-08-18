# MDSplus device support on acq400 series digitizers

MDSplus now supports python based devices. This document outlines how to install the latest MDSplus device code for use with D-TACQ acq400 series devices.

NB: older versions MDSplus depend on python2, not python3; if this is the case, please substitute "python2" for "python3" in the examples..

# Code installation

There are a few repositories that will need to be installed first. The relevant repositories should be installed in ~/PROJECTS/. To create a ~/PROJECTS/ folder just run the following code:

The PC should have MDSplus installed in the normal way at /usr/local/mdsplus

## Clone the tree support repository


    git clone https://github.com/D-TACQ/ACQ400_MDSplus_TREESUPPORT.git ~/PROJECTS/

### Install all other projects, including HAPI

    cd PROJECTS/ACQ400_MDSplus_TREESUPPORT
    ./install_acq400_mdsplus.sh


## Installing a tree with a new MDSplus device node

There is a script to create MDSplus device trees. If the user wishes to use MDSTCL to install the trees this is also possible and the steps are very similar to the python, however the python automates a lot of the steps like checking channel counts. Note that the script will install the tree by default in ~/TREES/. An example command line would be something like:

    python ./make_acq400_device.py --model=tr --name='TR' --carrier=acq2106 acq2106_201

This will print some messages about how MDSplus needs the user to add information to the path. It is possible to automate this as well for many UUTs:
```bash
    for uut in {201..226}; 
    	do echo "acq2106_${uut}_path /home/dt100/TREES/acq2106_${uut}" | sudo tee -a /usr/local/mdsplus/local/envsyms; 
    	export acq2106_${uut}_path=/home/dt100/TREES/acq2106_$uut; 
    	python ./make_acq400_device.py --model=tr --name=TR acq2106_${uut}; 
    done
```

## Viewing data using jScope

Once a shot has been taken the data visualisation can be done using jScope. The user can use the jscope-uutpanel-gen.py. This relies on a 'default.jscp' being available in ~/jScope/configurations/.

### Creating a default.jscp

The jScope program comes with MDSplus, but a default.jscp file is what gets loaded by default in jScope, but saved to disk. So to create a default.jscp the user would start jScope as normal and then immediately press 'customize' -> 'save current settings as ' and then save as default.jscp.

### Using jscope-uutpanel-gen.py

Once this is done the user can create custom jscp files for use with jScope. The syntax for doing so is as shown below:

    python ./jscope-uutpanel-gen.py --node=TR --nchan=8 $UUTS > ~/jScope/configurations/zap318.8.jscp

The newly created acq2106_mr.jscp can then be loaded from jScope by selecting 'customize' -> 'use saved settings from' and then choosing acq2106_mr.jscp.
