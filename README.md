# labctrl
a304/b20

## To add a new device

First, implement the RESTful API for the new device in "servers", also provide an emulator if possible.

Assign a new port to your API and add it to the table in servers/README.md

Add a json config file of the new device in "configs". The config file must include the API host and port for the new device.

Add remote API caller classes in "components" to provide local API.

Add the corresponding factory class in "components" to provide UI widgets of the device. Factory for Bokeh UI widgets are prefered because it is web-based

## To add a new method

First, determine the components needed for the method. Specify them at the beginning of your method program.

Assign a new method name and short name in "configs/methods", put method specific settings there

Implement the method unit operation and thread task in "methods"

