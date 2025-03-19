import { importAuthFromFile_impl } from "./import_auth";

/**
 * Class mirroring the structure of the `auth.json` file from `userdata/auth/`
 */
export class Auth {
    "novelai" = {
        mail: "",
        password: "",
        api_key: "",
        use_api_key: false,
    };
    "openai" = {
        token: "",
    };
    "characterai" = {
        token: "",
    };
    "twitch" = {
        channel_name: "",
        oauth_token: "",
        twitchapp_clientid: "",
        twitchapp_secret: "",
    };
    "azure" = {
        token: "",
        region: "",
    };

    static AUTH_PATH = process.cwd() + "/userdata/auth/auth.json";
    /** @see `./import_auth.ts` */
    static importFromFile: () => Auth = importAuthFromFile_impl;
}
