import { Dependencies } from "../dependencies/dependencies";
import { getVersion_impl } from "../version/version";
import { mainLoop_impl } from "../main_loop/main_loop";
import { AppState } from "../state/state";
import { Plugin } from "../plugins/plugin";

// The actual Python path is determined at runtime by checking environment
// The INSTALL.bat script will try to find Python 3.9 specifically
export const ENV = {
    // Default to 'python', but the application will try to detect Python 3.9
    // during installation and set the actual path in INSTALL.bat
    PYTHON_PATH: "python",
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
