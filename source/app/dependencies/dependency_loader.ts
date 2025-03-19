import { Result } from "../types/Result";
import { ENV, wAIfu } from "../types/Waifu";
import { Dependency_T, Dependencies } from "../types/Dependency";
import { IO } from "../io/io";

import { TextToSpeechLocalAI } from "../tts/tts_localai";
import { TextToSpeechPyttsx3 } from "../tts/tts_pyttsx3";
import { TextToSpeechNovelAI } from "../tts/tts_novelai";
import { TextToSpeechElevenLabs } from "../tts/tts_elevenlabs";
import { TextToSpeechCoquiTTS } from "../tts/tts_coquitts";
import { TextToSpeechNovelAIDirect } from "../tts/tts_novelai_direct";
import { TextToSpeechOpeanAITTS } from "../tts/tts_openai_tts";
import { TextToSpeechGoogleTTS } from "../tts/tts_google";
import { TextToSpeechAzureTTS } from "../tts/tts_azure";
import { TextToSpeechSpeechifyTTS } from "../tts/tts_speechify";
import { TextToSpeechNovelAIEnhanced } from "../tts/tts_novelai_enhanced";

import { LargeLanguageModelChatGPT35 } from "../llm/llm_chatgpt_35";
import { LargeLanguageModelChatGPT4 } from "../llm/llm_chatgpt_4";
import { LargeLanguageModelClaude } from "../llm/llm_claude";
import { LargeLanguageModelLlamacpp } from "../llm/llm_llamacpp";
import { LargeLanguageModelOoba } from "../llm/llm_ooba";
import { LargeLanguageModelLocalAI } from "../llm/llm_localai";
import { LargeLanguageModelNovelAI } from "../llm/llm_novelai";
import { LargeLanguageModelNovelAIDirect } from "../llm/llm_novelai_direct";
import { LargeLanguageModelNovelAIEnhanced } from "../llm/llm_novelai_enhanced";
import { LargeLanguageModelXMChat } from "../llm/llm_xmchat";
import { LargeLanguageModelPaLM } from "../llm/llm_palm";
import { LargeLanguageModelCohereWebAPI } from "../llm/llm_cohere";
import { LargeLanguageModelKoboldCPP } from "../llm/llm_koboldcpp";
import { LargeLanguageModelOllamaCLI } from "../llm/llm_ollama_cli";
import { LargeLanguageModelOllamaAPI } from "../llm/llm_ollama_api";
import { LargeLanguageModelPerplexity } from "../llm/llm_perplexity";

import { SpeechToTextWhisper } from "../stt/stt_whisper";
import { SpeechToTextAzure } from "../stt/stt_azure";
import { SpeechToTextWebspeech } from "../stt/stt_webspeech";

import { VoiceInputPyAudio } from "../voice_input/voice_input_pyaudio";

import { DiscordClient } from "../integrations/discord";
import { TwitchClient } from "../integrations/twitch";
import { VtubeStudioIntegration } from "../integrations/vtube_studio";

export function get_tts_default_values(
    name: string
): undefined | Record<string, any> {
    const result: undefined | Record<string, any> = undefined;
    return result;
}

export function load_dependencies(): Promise<Result<Dependencies, string>> {
    return new Promise((resolve) => {
        async function SAFE_LOADER() {
            const loaded_dependencies: Dependencies = {} as Dependencies;

            //
            // ---------- TTS ----------
            //

            if (
                wAIfu.state!.config.text_to_speech.provider.value ===
                "local_ai_text_to_speech"
            ) {
                loaded_dependencies.tts = new TextToSpeechLocalAI();
            } else if (
                wAIfu.state!.config.text_to_speech.provider.value === "pytts"
            ) {
                loaded_dependencies.tts = new TextToSpeechPyttsx3();
            } else if (
                wAIfu.state!.config.text_to_speech.provider.value === "novelai"
            ) {
                loaded_dependencies.tts = new TextToSpeechNovelAI();
            } else if (
                wAIfu.state!.config.text_to_speech.provider.value ===
                "novelai_direct"
            ) {
                if (wAIfu.state!.config.text_to_speech.novelai_use_enhanced.value) {
                    loaded_dependencies.tts = new TextToSpeechNovelAIEnhanced();
                } else {
                    loaded_dependencies.tts = new TextToSpeechNovelAIDirect();
                }
            } else if (
                wAIfu.state!.config.text_to_speech.provider.value === "elevenlabs"
            ) {
                loaded_dependencies.tts = new TextToSpeechElevenLabs();
            } else if (
                wAIfu.state!.config.text_to_speech.provider.value === "coqui-tts"
            ) {
                loaded_dependencies.tts = new TextToSpeechCoquiTTS();
            } else if (
                wAIfu.state!.config.text_to_speech.provider.value ===
                "openai_text_to_speech"
            ) {
                loaded_dependencies.tts = new TextToSpeechOpeanAITTS();
            } else if (
                wAIfu.state!.config.text_to_speech.provider.value ===
                "google_text_to_speech"
            ) {
                loaded_dependencies.tts = new TextToSpeechGoogleTTS();
            } else if (
                wAIfu.state!.config.text_to_speech.provider.value ===
                "azure_text_to_speech"
            ) {
                loaded_dependencies.tts = new TextToSpeechAzureTTS();
            } else if (
                wAIfu.state!.config.text_to_speech.provider.value ===
                "speechify_text_to_speech"
            ) {
                loaded_dependencies.tts = new TextToSpeechSpeechifyTTS();
            } else {
                console.warn(
                    `WARNING: Configuration for tts Provider '${wAIfu.state!.config.text_to_speech.provider.value}' not recognized.`
                );
                loaded_dependencies.tts = null;
            }

            //
            // ---------- LLM ----------
            //

            if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "chatgpt35"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelChatGPT35();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "chatgpt4"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelChatGPT4();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "claude"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelClaude();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "llamacpp"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelLlamacpp();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "koboldcpp"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelKoboldCPP();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value === "ooba"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelOoba();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "local_ai"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelLocalAI();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "novelai"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelNovelAI();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "novelai_direct"
            ) {
                if (wAIfu.state!.config.large_language_model.novelai_use_enhanced.value) {
                    loaded_dependencies.llm = new LargeLanguageModelNovelAIEnhanced();
                } else {
                    loaded_dependencies.llm = new LargeLanguageModelNovelAIDirect();
                }
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "xmchat"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelXMChat();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value === "palm"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelPaLM();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "ollama_cli"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelOllamaCLI();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "ollama_api"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelOllamaAPI();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "cohere"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelCohereWebAPI();
            } else if (
                wAIfu.state!.config.large_language_model.provider.value ===
                "perplexity"
            ) {
                loaded_dependencies.llm = new LargeLanguageModelPerplexity();
            } else {
                console.warn(
                    `WARNING: Configuration for LLM Provider '${wAIfu.state!.config.large_language_model.provider.value}' not recognized.`
                );
                loaded_dependencies.llm = null;
            }

            //
            // ---------- STT ----------
            //

            if (
                wAIfu.state!.config.speech_to_text.provider.value === "whisper" &&
                wAIfu.state!.config.primary.voice_input.value === true
            ) {
                loaded_dependencies.stt = new SpeechToTextWhisper();
            } else if (
                wAIfu.state!.config.speech_to_text.provider.value === "azure" &&
                wAIfu.state!.config.primary.voice_input.value === true
            ) {
                loaded_dependencies.stt = new SpeechToTextAzure();
            } else if (
                wAIfu.state!.config.speech_to_text.provider.value ===
                    "webspeech" &&
                wAIfu.state!.config.primary.voice_input.value === true
            ) {
                loaded_dependencies.stt = new SpeechToTextWebspeech();
            } else {
                loaded_dependencies.stt = null;
            }

            //
            // ---------- MIC CAPTURE ----------
            //

            if (
                wAIfu.state!.config.speech_to_text.provider.value !== "webspeech" &&
                wAIfu.state!.config.primary.voice_input.value === true
            ) {
                loaded_dependencies.mic = new VoiceInputPyAudio();
            } else {
                loaded_dependencies.mic = null;
            }

            //
            // ---------- DISCORD ----------
            //

            if (wAIfu.state!.config.integrations.discord.use_discord.value) {
                loaded_dependencies.discord = new DiscordClient();
            } else {
                loaded_dependencies.discord = null;
            }

            //
            // ---------- TWITCH ----------
            //

            if (wAIfu.state!.config.integrations.twitch.use_twitch.value) {
                loaded_dependencies.twitch = new TwitchClient();
            } else {
                loaded_dependencies.twitch = null;
            }

            //
            // ---------- VTUBE STUDIO ----------
            //

            if (wAIfu.state!.config.primary.use_vts.value) {
                loaded_dependencies.vts = new VtubeStudioIntegration();
            } else {
                loaded_dependencies.vts = null;
            }

            //
            // ---------- INITIALIZATION ----------
            //
            const tts_load = loaded_dependencies.tts === null ? true : false;
            const llm_load = loaded_dependencies.llm === null ? true : false;
            const stt_load = loaded_dependencies.stt === null ? true : false;
            const mic_load = loaded_dependencies.mic === null ? true : false;
            const twitch_load =
                loaded_dependencies.twitch === null ? true : false;
            const discord_load =
                loaded_dependencies.discord === null ? true : false;
            const vts_load = loaded_dependencies.vts === null ? true : false;

            const init_tasks: Promise<void>[] = [];

            if (!tts_load)
                init_tasks.push(
                    loaded_dependencies.tts!.initialize().then(() => {
                        IO.success(`TTS: loaded.`);
                    })
                );
            if (!llm_load)
                init_tasks.push(
                    loaded_dependencies.llm!.initialize().then(() => {
                        IO.success(`LLM: loaded.`);
                    })
                );
            if (!stt_load && wAIfu.state!.config.primary.voice_input.value)
                init_tasks.push(
                    loaded_dependencies.stt!.initialize().then(() => {
                        IO.success(`STT: loaded.`);
                    })
                );
            if (!mic_load && wAIfu.state!.config.primary.voice_input.value)
                init_tasks.push(
                    loaded_dependencies.mic!.initialize().then(() => {
                        IO.success(`MIC: loaded.`);
                    })
                );
            if (!discord_load)
                init_tasks.push(
                    loaded_dependencies.discord!.initialize().then(() => {
                        IO.success(`DISCORD: loaded.`);
                    })
                );
            if (!twitch_load)
                init_tasks.push(
                    loaded_dependencies.twitch!.initialize().then(() => {
                        IO.success(`TWITCH: loaded.`);
                    })
                );
            if (!vts_load)
                init_tasks.push(
                    loaded_dependencies.vts!.initialize().then(() => {
                        IO.success(`VTS: loaded.`);
                    })
                );

            await Promise.all(init_tasks);

            resolve(new Result(true, loaded_dependencies, ""));
        }

        try {
            SAFE_LOADER().catch((err) => {
                console.error(err);
                resolve(
                    new Result(false, {} as Dependencies, "Some error occured.")
                );
            });
        } catch (err) {
            console.error(err);
            resolve(
                new Result(false, {} as Dependencies, "Some error occured.")
            );
        }
    });
}
