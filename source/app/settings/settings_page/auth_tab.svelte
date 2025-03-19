<!-- Auth Tab -->
<script lang="ts">
    import { onMount } from "svelte";
    import { wAIfu } from "../../types/Waifu";
    import { writeAuthToFile } from "../../file_system/write_to_disk";
    import { IO } from "../../io/io";
    import Checkbox from "../checkbox.svelte";

    const mailRegex = new RegExp(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/);
    const tokenRegex = new RegExp(/^[a-zA-Z0-9-_]+$/);

    // Empty fields
    let nai_mail = "";
    let nai_pwd = "";
    let nai_api_key = "";
    let nai_use_api_key = false;

    let api_token = "";
    let cai_token = "";
    let azure_token = "";
    let azure_region = "";

    let twitch_channel = "";
    let twitch_token = "";
    let twitch_clientid = "";
    let twitch_secret = "";

    onMount(() => {
        nai_mail = wAIfu.state!.auth["novelai"]["mail"];
        nai_pwd = wAIfu.state!.auth["novelai"]["password"];
        nai_api_key = wAIfu.state!.auth["novelai"]["api_key"];
        nai_use_api_key = wAIfu.state!.auth["novelai"]["use_api_key"];

        api_token = wAIfu.state!.auth["openai"]["token"];
        cai_token = wAIfu.state!.auth["characterai"]["token"];
        azure_token = wAIfu.state!.auth["azure"]["token"];
        azure_region = wAIfu.state!.auth["azure"]["region"];

        twitch_channel = wAIfu.state!.auth["twitch"]["channel_name"];
        twitch_token = wAIfu.state!.auth["twitch"]["oauth_token"];
        twitch_clientid = wAIfu.state!.auth["twitch"]["twitchapp_clientid"];
        twitch_secret = wAIfu.state!.auth["twitch"]["twitchapp_secret"];
    });

    const save = () => {
        // Validate mail & password
        if (nai_mail.length > 0 && nai_pwd.length > 0) {
            if (mailRegex.test(nai_mail) === false) {
                window.alert("Invalid NovelAI mail!");
                return;
            }
        }

        // NovelAI
        wAIfu.state!.auth["novelai"]["mail"] = nai_mail;
        wAIfu.state!.auth["novelai"]["password"] = nai_pwd;
        wAIfu.state!.auth["novelai"]["api_key"] = nai_api_key;
        wAIfu.state!.auth["novelai"]["use_api_key"] = nai_use_api_key;

        // OpenAI
        wAIfu.state!.auth["openai"]["token"] = api_token;

        // CharacterAI
        wAIfu.state!.auth["characterai"]["token"] = cai_token;

        // Azure
        wAIfu.state!.auth["azure"]["token"] = azure_token;
        wAIfu.state!.auth["azure"]["region"] = azure_region;

        // Twitch
        wAIfu.state!.auth["twitch"]["channel_name"] = twitch_channel;
        wAIfu.state!.auth["twitch"]["oauth_token"] = twitch_token;
        wAIfu.state!.auth["twitch"]["twitchapp_clientid"] = twitch_clientid;
        wAIfu.state!.auth["twitch"]["twitchapp_secret"] = twitch_secret;

        // Save changes to disk
        writeAuthToFile(wAIfu.state!.auth);
        IO.debug("Saved auth infos.");

        // Update UI
        if (document.getElementById("auth_update")) {
            (document.getElementById("auth_update") as HTMLElement).style.opacity =
                "1";
            // @ts-ignore
            auth_update_timeout = setTimeout(() => {
                if (document.getElementById("auth_update")) {
                    (
                        document.getElementById(
                            "auth_update"
                        ) as HTMLElement
                    ).style.opacity = "0";
                }
            }, 1500);
        }

        return;
    };

    let auth_update_timeout: NodeJS.Timeout | undefined = undefined;
</script>

<div class="tab_content">
    <h3>Accounts</h3>
    <p>
        Enter your login details for w-AI-fu to use.
        Only fill in the details for the services you want to use.
    </p>
    <br /><br />

    <div class="section">
        <h4>NovelAI</h4>
        <label for="nai_mail">Email</label>
        <input
            type="text"
            name="nai_mail"
            placeholder="novelai email"
            bind:value={nai_mail}
        />
        <label for="nai_pwd">Password</label>
        <input
            type="password"
            name="nai_pwd"
            placeholder="novelai password"
            bind:value={nai_pwd}
        />
        <label for="nai_api_key">API Key</label>
        <input
            type="password"
            name="nai_api_key"
            placeholder="novelai api key"
            bind:value={nai_api_key}
        />
        <div class="checkbox-container">
            <Checkbox bind:checked={nai_use_api_key} />
            <label for="nai_use_api_key">Use API Key (preferred method)</label>
        </div>
        <div class="hint-text">
            <p>
                You can find your API key in your NovelAI account settings. 
                Using an API key is the recommended authentication method as it's more reliable.
            </p>
        </div>
    </div>

    <div class="section">
        <h4>OpenAI</h4>
        <label for="api_token">API Token</label>
        <input
            type="password"
            name="api_token"
            placeholder="openai token"
            bind:value={api_token}
        />
    </div>

    <div class="section">
        <h4>CharacterAI</h4>
        <label for="cai_token">Token</label>
        <input
            type="password"
            name="cai_token"
            placeholder="characterai token"
            bind:value={cai_token}
        />
    </div>

    <div class="section">
        <h4>Azure</h4>
        <label for="azure_token">API Token</label>
        <input
            type="password"
            name="azure_token"
            placeholder="azure token"
            bind:value={azure_token}
        />
        <label for="azure_region">Region</label>
        <input
            type="text"
            name="azure_region"
            placeholder="azure region"
            bind:value={azure_region}
        />
    </div>

    <div class="section">
        <h4>Twitch</h4>
        <label for="twitch_channel">Channel name</label>
        <input
            type="text"
            name="twitch_channel"
            placeholder="Channel name"
            bind:value={twitch_channel}
        />

        <label for="twitch_token">OAuth Token</label>
        <input
            type="password"
            name="twitch_token"
            placeholder="Twitch token"
            bind:value={twitch_token}
        />

        <label for="twitch_clientid">Client ID</label>
        <input
            type="text"
            name="twitch_clientid"
            placeholder="Twitch client ID"
            bind:value={twitch_clientid}
        />

        <label for="twitch_secret">Client Secret</label>
        <input
            type="password"
            name="twitch_secret"
            placeholder="Twitch client secret"
            bind:value={twitch_secret}
        />
    </div>

    <br />
    <div class="btn_container">
        <button class="btn" on:click={save}>Save</button>
        <span id="auth_update" style="opacity: 0;">Updated!</span>
    </div>
</div>

<style>
    .tab_content {
        max-width: 100%;
        max-height: 100%;
        padding: 0 1em;
        box-sizing: border-box;
        overflow-y: auto;
    }

    .section {
        margin-bottom: 2rem;
        padding: 1rem;
        border-radius: 5px;
        background-color: #2a2a2a;
    }

    h3 {
        margin-top: 0;
    }

    h4 {
        margin-top: 0;
        margin-bottom: 1rem;
        color: #cccccc;
    }

    p {
        margin-bottom: 1em;
        color: #aaaaaa;
    }

    label {
        display: block;
        margin-bottom: 0.5em;
        color: #dddddd;
    }

    input {
        width: 100%;
        padding: 0.5em;
        margin-bottom: 1em;
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #444444;
        border-radius: 3px;
    }

    input:focus {
        outline: none;
        border-color: #555555;
    }

    .btn_container {
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .btn {
        padding: 0.5em 1em;
        margin-right: 1em;
        background-color: #444444;
        color: #ffffff;
        border: none;
        border-radius: 3px;
        cursor: pointer;
    }

    .btn:hover {
        background-color: #555555;
    }

    #auth_update {
        color: #ffffff;
        transition: opacity 0.3s ease;
    }

    .checkbox-container {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }

    .checkbox-container label {
        margin-left: 0.5rem;
        margin-bottom: 0;
    }

    .hint-text {
        margin-top: 0.5rem;
        font-size: 0.9rem;
        color: #aaaaaa;
    }

    .hint-text p {
        margin-bottom: 0.5rem;
    }
</style>
