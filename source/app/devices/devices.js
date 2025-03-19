"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDeviceIndex = exports.getDevices = void 0;
const cproc = __importStar(require("child_process"));
const Waifu_1 = require("../types/Waifu");
const io_1 = require("../io/io");
function getDevices() {
    try {
        let proc = cproc.spawnSync(Waifu_1.ENV.PYTHON_PATH, ["audio_devices.py"], {
            cwd: process.cwd() + "/source/app/devices/",
            shell: false,
        });
        
        let err = proc.stderr;
        if (err !== null) {
            let err_str = err.toString("utf8");
            if (err_str !== "") {
                io_1.IO.error(err_str);
                // Return empty object for error case
                return {};
            }
        }
        
        let output = proc.stdout;
        if (!output || output.length === 0) {
            io_1.IO.warn("No audio devices found or voice input disabled");
            return {};
        }
        
        const outputStr = output.toString("utf8");
        
        // Handle potential empty or invalid JSON
        try {
            return JSON.parse(outputStr);
        } catch (e) {
            io_1.IO.error("Failed to parse audio devices: " + e.message);
            io_1.IO.debug("Raw output was: " + outputStr);
            return {};
        }
    } catch (e) {
        io_1.IO.error("Failed to get audio devices: " + e.message);
        return {};
    }
}
exports.getDevices = getDevices;
function getDeviceIndex(device_name) {
    if (!Waifu_1.wAIfu.state || !Waifu_1.wAIfu.state.devices) {
        return 0;
    }
    return Waifu_1.wAIfu.state.devices[device_name] || 0;
}
exports.getDeviceIndex = getDeviceIndex;
