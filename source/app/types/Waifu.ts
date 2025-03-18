import { Dependencies } from "../dependencies/dependencies";
import { getVersion_impl } from "../version/version";
import { mainLoop_impl } from "../main_loop/main_loop";
import { AppState } from "../state/state";
import { Plugin } from "../plugins/plugin";

// Using Python 3.9 specifically
export const ENV = {
    PYTHON_PATH: "python3.9", // Will be overridden by the INSTALL.bat script with the actual path
};

export class WaifuApp {
    version: string = "";
    getVersion = getVersion_impl;
    mainLoop = mainLoop_impl;
    state: AppState | undefined = undefined;
    dependencies: Dependencies | undefined = undefined;
    plugins: Plugin[] = [];
}

export const wAIfu = new WaifuApp();
