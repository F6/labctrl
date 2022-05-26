/* globals feather:false */

function close_window() {
  if (confirm("Close Window? Currently running tasks will continue to run in the backend until finish, you will not lose your configs or saved data. If you need to terminate currently running tasks, use Terminate buttons, or simply kill the server.")) {
    close();
  }
}


function print_about() {
  alert("    LabCtrl version 20211206. This software is available directly from github https://github.com/F6/labctrl as git repo or zip file.\n    If you encounter any problem, feel free to contact me for help.\n    This software starts as an effort to provide consistent, well-documented programming interfaces for various instruments in our ultrafast laser lab to accelerate the development of new instruments and methods, because the old LabView APIs and programs are suprisingly hard to read and modify.\n    Python, C++ and JavaScript are chosen as the primary language used for this project, but I think adequate support for adapting other language modules are supported because nearly everything is passed around as JSON and YAML, thus it should be relatively easy to interface with existing code including our old APIs in LabView, in case you still need them.\n    If you need to add new components or methods to existing software, refer to README.md in source code directory.\n                   --Zhi Zi\n           December 2021 at Peking University");
}


(function () {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

})()

