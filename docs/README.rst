################
IoT project nr 7
################

This project was created for 'Internet of Things' course in AGH University.
It's meant to design and test algorithm for arrangement of computational processes in IoT network.
Simulated scenario is network of city's cameras and analysis of video material they provide.

Creators:
=========

Paweł Marszał

Jakub Nowobilski

Patryk Skupień

Jakub Wydra

General information
===================

Devices - agents
----------------

Network is built from connected devices.
Each of them has some computing power (measured in Units / unit of time), can communicate with other devices and perform computations.

Devices are grouped into 4 categories:

0) cloud            - single, very powerful server that can perform basically any computation in no time

1) regional server  - groups some number of local servers, with more computational power than each of them

2) local server     - smallest server in our network, it receives tasks (video material) from cameras

3) camera           - has no computational power, it's function is to provide servers with tasks to perform

General structure of network looks as follows (from top to bottom):

WSTAW OBRAZEK Z DRZEWEM

Every camera has exactly one server as it's parent.

Tasks
-----

Tasks to compute are main subject in this project.
Cameras generate them randomly based on configuration, and send them to their servers.
Every task has specified number of computing units necessary to complete it, and maximum time it needs to be completed in.

Important assumption in our simulation is that every task can be divide in any manner, and that sending them between different devices takes no time.

Algorithm
=========

We decided that main rule of our algorithm will be maximization of usage of local servers.

Our algorithm is as follows:

- when device receives task to compute, it checks if it can compute all of it in required time.

    - if it can, task is subscribed on TODO list, assigned some part of device's computational power and is being computed in some time

        - after completion result is generated

    - if it cannot, device ask its neighbours if they can do it. then task is divided between itself and said neighbours.

        - if there is still some part of the task left, that cannot be computed by any of device's neighbours, it's send up to device's parent

        - after division of a task, device waits for all partial results and then combines them into one result

- after result is ready (either generated or combined from parts) it is send back to its source device

Visualization
=============

Technology
----------

WRITE SOMETHING ABOUT LIBRARY AND STUFF

Examples
--------

INSERT SOME PHOTOS

Some statistics
===============

We decided that good measure of effectiveness of our algorithm will be average usage of computational power of devices in the network.

WRITE SOMETHING MORE

INSERT SOME GRAPHS
