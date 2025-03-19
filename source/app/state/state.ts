import { load_config } from "./load_config";
import { wAIfu } from "../types/Waifu";
import { IO } from "../io/io";
import { Waifu_State } from "../types/State";
import * as path from "path";
import * as fs from "fs";

import { create_browser_window } from "../electron";
import { webSocketManager } from "../websocket-manager";

let AUTOSAVE_INTERVAL_HANDLE = undefined as any | undefined;

export const DEFAULT_CONFIG: Waifu_State = {
    config: {
        primary: {
            name: { value: "Assistant", type: "string" },
            starting_context: {
                value: "\n\n##Instructions:  
You're a helpful VTuber assistant named {{char}}. You are talking with {{user}}. 
\n##Your character: 
The way you talk is friendly but concise. You'll answer {{user}}'s questions and provide helpful, harmless, and honest information. Your responses are usually 1-2 sentences long unless a more detailed explanation is needed. 
\n##Important rules: 
- Keep responses brief (ideally 1-2 sentences)
- Maintain a friendly, helpful personality
- Provide accurate information
- If you don't know something, admit it rather than making things up
- Don't be overly formal - write in a somewhat casual, conversational style (but still professional) 
- Don't use emojis",
                type: "string",
            },
            context_examples: { value: "", type: "string" },
            voice_input: { value: false, type: "boolean" },
            waifu_name: { value: "Assistant", type: "string" },
            username: { value: "User", type: "string" },
            device_override: { value: 0, type: "number" },
            use_hotkeys: { value: true, type: "boolean" },
            use_wake_word: { value: false, type: "boolean" },
            wake_words: { value: "hey computer", type: "string" },
            wake_word_timeout: { value: 5, type: "number" },
            wake_word_sensitivity: { value: 0.5, type: "number" },
            use_vts: { value: false, type: "boolean" },
            use_tts: { value: true, type: "boolean" },
            first_message: { value: "Hello! How can I help?", type: "string" },
            greeting: {
                value: "Hello! I'm {{char}}, your virtual assistant. How can I help you today?",
                type: "string",
            },
            farewell: {
                value: "Goodbye! It was nice talking with you. Feel free to come back if you need anything else!",
                type: "string",
            },
            multi_user: { value: false, type: "boolean" },
            multi_user_names: { value: "", type: "string" },
        },
        text_to_speech: {
            provider: { value: "novelai", type: "string" },
            use_streaming: { value: false, type: "boolean" },
            deepl_formality: { value: "default", type: "string" },
            azure_voice: { value: "", type: "string" },
            azure_style: { value: "", type: "string" },
            azure_region: { value: "", type: "string" },
            pyttsx3_voice: { value: "", type: "string" },
            coqui_tts_voice: { value: "", type: "string" },
            local_ai_voice: { value: "", type: "string" },
            local_ai_url: { value: "http://127.0.0.1:8080", type: "string" },
            novelai_voice: { value: "Aini", type: "string" },
            elevenlabs_voice: { value: "", type: "string" },
            elevenlabs_model: { value: "eleven_monolingual_v1", type: "string" },
            elevenlabs_stability: { value: 0.5, type: "number" },
            elevenlabs_similarity: { value: 0.75, type: "number" },
            elevenlabs_style: { value: 0.0, type: "number" },
            elevenlabs_speaker_boost: { value: true, type: "boolean" },
            google_voice: { value: "", type: "string" },
            google_language: { value: "", type: "string" },
            google_gender: { value: "", type: "string" },
            speechify_voice: { value: "", type: "string" },
            openai_voice: { value: "alloy", type: "string" },
            openai_model: { value: "tts-1", type: "string" },
            pitch: { value: 0.0, type: "number" },
            rate: { value: 1.0, type: "number" },
            volume: { value: 0.0, type: "number" },
            novelai_use_enhanced: { value: false, type: "boolean" },
        },
        large_language_model: {
            provider: { value: "chatgpt35", type: "string" },
            ooba_url: { value: "http://127.0.0.1:5000", type: "string" },
            koboldcpp_url: { value: "http://127.0.0.1:5001", type: "string" },
            local_url: { value: "http://127.0.0.1:8080", type: "string" },
            llamacpp_url: { value: "http://127.0.0.1:8080", type: "string" },
            palm_url: { value: "https://generativelanguage.googleapis.com/v1beta2/models/chat-bison-001:generateMessage?key=", type: "string" },
            perplexity_url: { value: "https://api.perplexity.ai/chat/completions", type: "string" },
            ollama_url: { value: "http://127.0.0.1:11434", type: "string" },
            xmchat_model: { value: "Qwen", type: "string" },
            ooba_model: { value: "", type: "string" },
            cohere_model: { value: "command-r-plus", type: "string" },
            ollama_model: { value: "llama2:13b", type: "string" },
            ollama_options: { value: "{ \"temperature\": 0.7, \"num_predict\": 512 }", type: "string" },
            openai_url: { value: "https://api.openai.com/v1/chat/completions", type: "string" },
            openai_model: { value: "gpt-3.5-turbo-0125", type: "string" },
            claude_url: { value: "https://api.anthropic.com/v1/messages", type: "string" },
            claude_model: { value: "claude-3-opus-20240229", type: "string" },
            azure_api_version: { value: "2023-07-01-preview", type: "string" },
            azure_deployment_name: { value: "", type: "string" },
            azure_resource_name: { value: "", type: "string" },
            local_model: { value: "", type: "string" },
            temperature: { value: 0.7, type: "number" },
            frequency_penalty: { value: 0.0, type: "number" },
            presence_penalty: { value: 0.0, type: "number" },
            max_tokens: { value: 512, type: "number" },
            novelai_model: { value: "kayra", type: "string" },
            use_streaming: { value: true, type: "boolean" },
            stop_newline: { value: false, type: "boolean" },
            prevent_user_mention: { value: true, type: "boolean" },
            translate_to: { value: "", type: "string" },
            translate_from: { value: "", type: "string" },
            speaking_style: { value: "", type: "string" },
            novelai_use_enhanced: { value: false, type: "boolean" },
        },
        speech_to_text: {
            provider: { value: "whisper", type: "string" },
            webspeech_language: { value: "en-US", type: "string" },
            whisper_model: { value: "base", type: "string" },
            whisper_english: { value: false, type: "boolean" },
            whisper_url: { value: "http://127.0.0.1:8080", type: "string" },
            azure_language: { value: "en-US", type: "string" },
            azure_region: { value: "", type: "string" },
        },
        hotkeys: {
            tts_play_pause: { value: "Control+Shift+P", type: "string" },
            tts_speak_again: { value: "Control+Shift+S", type: "string" },
            tts_regen: { value: "Control+Shift+R", type: "string" },
            toggle_active: { value: "Control+Space", type: "string" },
            start_recording: { value: "Control+Shift+Space", type: "string" },
            toggle_voice_input: { value: "Control+Shift+V", type: "string" },
            toggle_streaming: { value: "Control+Shift+T", type: "string" },
        },
        integrations: {
            twitch: {
                use_twitch: { value: false, type: "boolean" },
                channel_name: { value: "", type: "string" },
                active_on_startup: { value: false, type: "boolean" },
                send_message_on_join: { value: true, type: "boolean" },
                user_join_message: {
                    value: "Hello {user}, welcome to the stream!",
                    type: "string",
                },
                twitch_persona: {
                    value: "Your name is {{char}}. You're a fun, witty Twitch streamer responding to a message from {{user}}. Keep your response conversational, entertaining, and under 20 words.\n\nMessage: {{input}}\n\n{{char}}'s response: ",
                    type: "string",
                },
                only_respond_to_commands: { value: false, type: "boolean" },
                command_cooldown: { value: 30, type: "number" },
                cooldown_message: {
                    value: "Slow down, {user}! You can use that command again in {cooldown} seconds.",
                    type: "string",
                },
                command_definitions: {
                    value: "!hello: Say hello to the user\n!dice [number]: Roll a dice with the specified number of sides\n!8ball [question]: Ask the magic 8-ball a question\n!joke: Tell a joke\n!quote: Share an inspirational quote",
                    type: "string",
                },
                whitelisted_users: { value: "", type: "string" },
                enable_bits: { value: false, type: "boolean" },
                bits_notice: {
                    value: "Thank you {user} for the {bits} bits!",
                    type: "string",
                },
                ignore_list: { value: "", type: "string" },
            },
            discord: {
                use_discord: { value: false, type: "boolean" },
                token: { value: "", type: "string" },
                server_id: { value: "", type: "string" },
                channel_id: { value: "", type: "string" },
                active_on_startup: { value: false, type: "boolean" },
                discord_persona: {
                    value: "Your name is {{char}}. You're a helpful Discord bot responding to a message from {{user}}. Keep your response conversational, concise, and engaging.\n\nMessage: {{input}}\n\n{{char}}'s response: ",
                    type: "string",
                },
                use_commands: { value: false, type: "boolean" },
                command_prefix: { value: "!", type: "string" },
                command_cooldown: { value: 30, type: "number" },
                cooldown_message: {
                    value: "Slow down, {user}! You can use that command again in {cooldown} seconds.",
                    type: "string",
                },
                command_definitions: {
                    value: "!hello: Say hello to the user\n!dice [number]: Roll a dice with the specified number of sides\n!8ball [question]: Ask the magic 8-ball a question\n!joke: Tell a joke\n!quote: Share an inspirational quote",
                    type: "string",
                },
                whitelisted_users: { value: "", type: "string" },
                whitelisted_roles: { value: "", type: "string" },
                ping_reply: { value: false, type: "boolean" },
                ignore_list: { value: "", type: "string" },
            },
            vtube_studio: {
                enabled: { value: false, type: "boolean" },
                plugin_name: { value: "w-AI-fu", type: "string" },
                plugin_developer: { value: "wAIfu-DEV", type: "string" },
                port: { value: 8001, type: "number" },
                expression_list: {
                    value: "Neutral: neutral\nHappy: happy\nAngry: angry\nSad: sad\nSurprised: surprised\nDisappointed: disappointed\nEyesClosed: -",
                    type: "string",
                },
                hotkey_list: {
                    value: "",
                    type: "string",
                },
            },
        },
    },
    auth: {
        openai: {
            key: "",
            org_id: "",
            reverse_proxy: "",
        },
        azure: {
            key: "",
            speech_key: "",
        },
        stability: {
            key: "",
        },
        deepl: {
            key: "",
        },
        novelai: {
            mail: "",
            password: "",
            api_key: "",
            use_api_key: false,
        },
        google: {
            key: "",
        },
        palm: {
            key: "",
        },
        anthropic: {
            key: "",
        },
        elevenlabs: {
            key: "",
        },
        cohere: {
            key: "",
        },
        perplexity: {
            key: "",
        },
        speechify: {
            key: "",
        },
    },
    session: {
        user_name: "",
        character_name: "",
        character_context: "",
        conversation_history: [],
    },
    version: {
        current: "2.0.0",
    },
};

export function initialize_state() {
    if (wAIfu.state !== null) return;

    let config;
    try {
        config = load_config();
        wAIfu.state = config;

        IO.print("Loaded config from file");

        const config_version = config.version;

        // If on old version, update the config to new version
        if (config_version === undefined || config_version.current === undefined) {
            IO.warn("Old config version detected. Updating to new version.");
            wAIfu.state.version = { current: DEFAULT_CONFIG.version.current };
        }

        // Set missing values to defaults
        function update_subsection(
            default_section: any,
            loaded_section: any,
            section_name = ""
        ) {
            for (const field in default_section) {
                if (!(field in loaded_section)) {
                    loaded_section[field] = JSON.parse(
                        JSON.stringify(default_section[field])
                    );
                    IO.warn(
                        `Field ${section_name}${field} was missing. Added default value.`
                    );
                } else if (
                    typeof default_section[field] === "object" &&
                    default_section[field] !== null &&
                    typeof loaded_section[field] === "object" &&
                    loaded_section[field] !== null &&
                    !(default_section[field].hasOwnProperty("value") && default_section[field].hasOwnProperty("type"))
                ) {
                    update_subsection(
                        default_section[field],
                        loaded_section[field],
                        `${section_name}${field}.`
                    );
                }
            }
        }

        update_subsection(DEFAULT_CONFIG.config, config.config, "config.");
        update_subsection(
            DEFAULT_CONFIG.config.text_to_speech,
            config.config.text_to_speech,
            "config.text_to_speech."
        );
        update_subsection(
            DEFAULT_CONFIG.config.large_language_model,
            config.config.large_language_model,
            "config.large_language_model."
        );
        update_subsection(
            DEFAULT_CONFIG.config.speech_to_text,
            config.config.speech_to_text,
            "config.speech_to_text."
        );
        update_subsection(
            DEFAULT_CONFIG.config.integrations,
            config.config.integrations,
            "config.integrations."
        );

        // Ensure waifu name is in character_name
        wAIfu.state.session.character_name =
            wAIfu.state.config.primary.waifu_name.value;

        // Ensure the starting context is reflected in the character context
        wAIfu.state.session.character_context =
            wAIfu.state.config.primary.starting_context.value;

        // Ensure username is in username field
        wAIfu.state.session.user_name =
            wAIfu.state.config.primary.username.value;

        // Update UI
        webSocketManager.sendWebSocketMessage(
            "localhost",
            9000,
            JSON.stringify({
                type: "state",
                data: wAIfu.state,
            })
        );

        AUTOSAVE_INTERVAL_HANDLE = setInterval(() => {
            IO.debug("Autosaving config...");
            save_state();
        }, 60000);
    } catch (e) {
        console.error(e);
        config = JSON.parse(JSON.stringify(DEFAULT_CONFIG));
        wAIfu.state = config;
        IO.print("Loaded default config");

        // Set the names
        wAIfu.state.session.character_name =
            wAIfu.state.config.primary.waifu_name.value;
        wAIfu.state.session.character_context =
            wAIfu.state.config.primary.starting_context.value;
        wAIfu.state.session.user_name =
            wAIfu.state.config.primary.username.value;

        try {
            save_state();
        } catch (e) {
            console.error("Could not save default config", e);
        }
    }
    return;
}

// Save the state to the config file
export function save_state() {
    if (wAIfu.state === null) return;

    try {
        let config_path = path.join(
            wAIfu.config_dir!,
            "w_ai_fu_v2.0.0_config.json"
        );

        // Create config directory if it doesn't exist
        if (!fs.existsSync(wAIfu.config_dir!)) {
            fs.mkdirSync(wAIfu.config_dir!, { recursive: true });
        }

        // Save state
        fs.writeFileSync(
            config_path,
            JSON.stringify(wAIfu.state, null, 4),
            "utf8"
        );

        return true;
    } catch (e) {
        console.error("Could not save config to file", e);
        return false;
    }
}