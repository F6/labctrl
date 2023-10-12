# A proposal to refactor some of the web APIs we have

A lot of our web APIs are run with vanilla python Flask dev servers. This decision was made in early stage of this project. Back then there's only a few choices and we have chosen Flask because it is the easiest and fastest to write and test.

Around 4 years ago FastAPI was out and quickly gained popularity because developing with FastAPI is even faster and less error-prone. After 4 years of developing, FastAPI is already used and tested in large scale and proved its efficiency and robostness.

So I think now it is the time that we migrate to FastAPI.

Benefits we get from switching to FastAPI:

* less code to write
* similar grammer with Flask APIs, migration is quite simple
* less errors on type conversion
* compliance with OpenAPI standards
* easy JWT auth
* gateway interface for production, other than the temporary dev server

Drawbacks:

* requires additional libraries to develop, dev env needs some upgrade
* requires additional libraries to deploy, before that all we need is just vanilla python and maybe pyserial
* not supported on older machines running OS like WindowsXP
* may be deprecated in the future if the company fails

Additionally, recently we have also introduced some really fast devices that transmits heavy loads from/to the server and requires a ton of calculation to process its data. We would also need a new way to handle these new devices.

For example, our new SDR sampling card transmits its data at 10 Gbps rate through PCI-e/USB interface and requires real-time interleaved digital FIR filter and summing of the data.

Another example is our new FROG which uses a neural network model to infer the E-field and phase of pulsed laser from collected data, and the inferred result needs to be examined with autocorrelation calculations, so both steps are extremely calculation-heavy, and the steps must be performed several times each second.

Yet another example is our DMD array that is under working. The DMD is used to construct a given light field (its official name is "Spatial Light Modulation") by displaying different patterns on the DMD. A beam analyzer is used to monitor the output light field, so we need to generate the feedback signal by reading data from the beam analyzer. Then we calculate the next pattern of the DMD array, transmit it to the DMD and read from beam analyzer again to see if the light field is stablized to what we want. All these steps must be finished in our server blazingly fast (the FPS is over 1000). So this is both extremely calculation-heavy and transmission-heavy.

Although we try to use BLAS, MKL and in-place memory operation as much as possible, python is still too slow to support these new applicaitons, and it is also frustrating and tedious to avoid memory allocation and movement. Python also lacks methods to directly interact with high speed peripherals (drivers).

To make our life easier, it is better to implement a dedicated library for these calculation-heavy and transmission-heavy tasks with rust/c++/cuda and create python bindings to the library.

To facilitate the development further, we use gRPC to build calculation-heavy tasks as distributed microservices and dispatch jobs asynchronously to relieve the calculation burden to multiple cores/machines.

## The Plan

Here is the plan:

Firstly, we will not replace all our servers immediately. The server code is only refactored when we want new functionalities.

Secondly, the architecture will be more clear and uniform to further reduce the burden on caller side.

Finally, some of the most calculation-heavy or transmission-heavy tasks will migrate to gRPC calls with Rust/C++ and Cuda backend.

When implementing the new server, we plan to make sure it supports the following new features:

* Mixed REST API and socket
    - Everything is JSON.
    - For retriving stuff like sensor data or current motor position, implement full RESTful API. These data are non-exclusive and can be read by multiple agents at the same time so no need to put any constraints.
    - For setting stuff like camera exposure time, implement RESTful API with "put" but internally buffered in a FIFO to handle request. This cannot be paralleled because generally only 1 sensor is attached to server and this resource cannot be shared.
    - For real-time controlling, offer both RESTful API and socket API. The socket API is opened by requesting a RESTful API like /motors/socket. Before, we have used HTTP long polling to indicate finishing of command, this causes moderate amount of delay when instructions are very frequent. A socket will significantly reduce delay and accelerate responses.
    - RESTful API for controlling is also implemented for the convenience of single time operations such as user manual tinkering, which does not require a precise time of finish returned.
    - Socket API also uses JSON to pass data.
* Authenticaiton
    - Our old API can be called from anyone within the local network, which is unsafe if we intend to expand our controll to internet
    - Json Web Token (JWT) is used to authenticate appropriate client so that only those authenticated clients can call corresponding API
    - SSL used to provide additional encryption to protect JWTs from MITM attacks.
* Fully asynchronous and distributed (cloud-native)
    - New API will not provide blocking operations (no HTTP long-polling), instead, use socket if timing is critical
    - A global state machine represents the status of the unique resource bound to our server
    - When unique resource is requested conflictly, request is queued and 202 accepted is returned to the later client rather than waiting for releasing. It is the client's responsibility to poll and check for finish.
* Support of external server management
    - Previously servers must be started one-by-one, which is not convenient when a lot of devices are attached to the same host
    - Ideally a GUI helper tool can be used to manage all the servers to be started. The GUI tool generates a launch configuration that the launcher can read, and the server laucher starts and manages all the server processes.
    - Support for automatic recovery if server go down accidentally.
* Support for logs and audit
    - Experimental logs can be keeped if required by the university or auditing department.
* Fully typed
* Mocked tests
    - Always implement the mocking object for the unique resource the server is bound to, so that the API can be tested without actually operating the resource.
* Discovery
    - A discovery service can be enabled to broadcast the server info to other devices on the same network.
    - Maybe add QUIC

## An example

This would be an example for actual implementation of a remotely controlled linear stage.

    linear_stage/main.py : main server app for REST api
        |- linear_stage/HAL.py : Hardware Abstraction Layer provides the class to access real device
        |- linear_stage/mock.py : provides mock objects for actual HAL, to test software without device
        |- linear_stage/state.py : provides state machine to store current state globally
        |- linear_stage/discovery.py : provides broadcasting functionalities

    API:
    GET     /               <=  {} 
                            =>  {"available_apis": [...]}
    GET     /axis/{i}       <=  {} 
                            =>  {
                                    "position": {
                                        "data": 12.512352,
                                        "unit": "mm"
                                    },
                                    "velocity": {
                                        "data": 1.00002,
                                        "unit": "mm/s"
                                    },
                                    ...
                                }
    GET     /axis/{i}/position      <= {}
                                    =>  {
                                            "position": {
                                                "data": 12.512352,
                                                "unit": "mm"
                                            },
                                        }

    PUT     /axis/{i}               <=  {
                                            "command": "moveabs",
                                            "position": {
                                                "data": 12.512352,
                                                "unit": "mm"
                                            },
                                        }
                                    =>  {
                                            "
                                        }

