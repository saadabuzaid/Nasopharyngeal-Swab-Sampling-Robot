
"use strict";

let MasterboardDataMsg = require('./MasterboardDataMsg.js');
let IOStates = require('./IOStates.js');
let RobotModeDataMsg = require('./RobotModeDataMsg.js');
let Analog = require('./Analog.js');
let RobotStateRTMsg = require('./RobotStateRTMsg.js');
let ToolDataMsg = require('./ToolDataMsg.js');
let Digital = require('./Digital.js');

module.exports = {
  MasterboardDataMsg: MasterboardDataMsg,
  IOStates: IOStates,
  RobotModeDataMsg: RobotModeDataMsg,
  Analog: Analog,
  RobotStateRTMsg: RobotStateRTMsg,
  ToolDataMsg: ToolDataMsg,
  Digital: Digital,
};
