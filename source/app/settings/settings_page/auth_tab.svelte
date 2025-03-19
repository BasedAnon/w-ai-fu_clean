<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  import { wAIfu } from "../../types/Waifu";
  import { IO } from "../../io/io";
  import { save_state } from "../../state/state";
  import PageTitle from "../components/page_title.svelte";
  import TextField from "../components/text_field.svelte";
  import Checkbox from "../components/checkbox.svelte";
  import Section from "../components/section.svelte";

  const dispatch = createEventDispatcher();

  let save_button_text = "Save";

  // OpenAI
  let openai_key = "";
  let openai_org_id = "";
  let openai_reverse_proxy = "";

  // Azure
  let azure_key = "";
  let azure_speech_key = "";

  // DeepL
  let deepl_key = "";

  // NovelAI
  let novelai_mail = "";
  let novelai_password = "";
  let novelai_api_key = "";
  let novelai_use_api_key = false;

  // Google
  let google_key = "";

  // Stability
  let stability_key = "";

  // PaLM
  let palm_key = "";

  // Anthropic
  let anthropic_key = "";

  // ElevenLabs
  let elevenlabs_key = "";

  // Cohereai
  let cohere_key = "";

  // Perplexity
  let perplexity_key = "";

  // Speechify
  let speechify_key = "";

  onMount(() => {
    if (wAIfu.state) {
      // OpenAI API key
      openai_key = wAIfu.state.auth.openai.key || "";

      // OpenAI org ID
      openai_org_id = wAIfu.state.auth.openai.org_id || "";

      openai_reverse_proxy = wAIfu.state.auth.openai.reverse_proxy || "";

      // Azure keys
      azure_key = wAIfu.state.auth.azure.key || "";
      azure_speech_key = wAIfu.state.auth.azure.speech_key || "";

      // DeepL API key
      deepl_key = wAIfu.state.auth.deepl.key || "";

      // NovelAI credentials
      novelai_mail = wAIfu.state.auth.novelai.mail || "";
      novelai_password = wAIfu.state.auth.novelai.password || "";
      novelai_api_key = wAIfu.state.auth.novelai.api_key || "";
      novelai_use_api_key = wAIfu.state.auth.novelai.use_api_key || false;

      // Google API key
      google_key = wAIfu.state.auth.google.key || "";

      // Stability API key
      stability_key = wAIfu.state.auth.stability.key || "";

      // PaLM api key
      palm_key = wAIfu.state.auth.palm.key || "";

      // Anthropic api key
      anthropic_key = wAIfu.state.auth.anthropic.key || "";

      // ElevenLabs api key
      elevenlabs_key = wAIfu.state.auth.elevenlabs.key || "";

      // Cohere API key
      cohere_key = wAIfu.state.auth.cohere.key || "";

      // Perplexity API key
      perplexity_key = wAIfu.state.auth.perplexity.key || "";

      // Speechify API key
      speechify_key = wAIfu.state.auth.speechify.key || "";
    }
  });

  function save_auth_config() {
    save_button_text = "Saving...";

    // OpenAI
    wAIfu.state.auth.openai.key = openai_key;
    wAIfu.state.auth.openai.org_id = openai_org_id;
    wAIfu.state.auth.openai.reverse_proxy = openai_reverse_proxy;

    // Azure
    wAIfu.state.auth.azure.key = azure_key;
    wAIfu.state.auth.azure.speech_key = azure_speech_key;

    // DeepL
    wAIfu.state.auth.deepl.key = deepl_key;

    // NovelAI
    wAIfu.state.auth.novelai.mail = novelai_mail;
    wAIfu.state.auth.novelai.password = novelai_password;
    wAIfu.state.auth.novelai.api_key = novelai_api_key;
    wAIfu.state.auth.novelai.use_api_key = novelai_use_api_key;

    // Google
    wAIfu.state.auth.google.key = google_key;

    // Stability
    wAIfu.state.auth.stability.key = stability_key;

    // PaLM
    wAIfu.state.auth.palm.key = palm_key;

    // Anthropic
    wAIfu.state.auth.anthropic.key = anthropic_key;

    // ElevenLabs
    wAIfu.state.auth.elevenlabs.key = elevenlabs_key;

    // Cohere
    wAIfu.state.auth.cohere.key = cohere_key;

    // Perplexity
    wAIfu.state.auth.perplexity.key = perplexity_key;

    // Speechify
    wAIfu.state.auth.speechify.key = speechify_key;

    try {
      const save_result = save_state();
      IO.print("Saved authentication configuration to disk.");
    } catch (e) {
      console.error(e);
      IO.error(
        "Failed to save authentication configuration to disk. See console for details."
      );
    }

    setTimeout(() => {
      save_button_text = "Save";
    }, 2000);
  }
</script>

<PageTitle name="Authentication" />

<div class="grid">
  <Section name="OpenAI">
    <TextField
      label="API Key"
      bind:value={openai_key}
      password={true}
      isVertical={true}
    />
    <TextField
      label="Organization ID (optional)"
      bind:value={openai_org_id}
      password={false}
      isVertical={true}
    />
    <TextField
      label="Reverse Proxy URL (optional)"
      bind:value={openai_reverse_proxy}
      password={false}
      isVertical={true}
    />
  </Section>

  <Section name="NovelAI">
    <TextField
      label="Account Email"
      bind:value={novelai_mail}
      password={false}
      isVertical={true}
    />
    <TextField
      label="Account Password"
      bind:value={novelai_password}
      password={true}
      isVertical={true}
    />
    <TextField
      label="API Key (alternative to using email/password)"
      bind:value={novelai_api_key}
      password={true}
      isVertical={true}
    />
    <Checkbox
      label="Use API Key"
      tooltip="If checked, uses the API Key instead of email/password"
      bind:checked={novelai_use_api_key}
    />
    <Checkbox
      label="Use Enhanced API (improved reliability)"
      tooltip="If checked, uses the enhanced Python API for improved reliability"
      bind:checked={wAIfu.state.config.text_to_speech.novelai_use_enhanced.value}
    />
  </Section>

  <Section name="Azure">
    <TextField
      label="API Key"
      bind:value={azure_key}
      password={true}
      isVertical={true}
    />
    <TextField
      label="Speech API Key"
      bind:value={azure_speech_key}
      password={true}
      isVertical={true}
    />
  </Section>

  <Section name="DeepL">
    <TextField
      label="API Key"
      bind:value={deepl_key}
      password={true}
      isVertical={true}
    />
  </Section>

  <Section name="Anthropic (Claude)">
    <TextField
      label="API Key"
      bind:value={anthropic_key}
      password={true}
      isVertical={true}
    />
  </Section>

  <Section name="Google">
    <TextField
      label="API Key"
      bind:value={google_key}
      password={true}
      isVertical={true}
    />
  </Section>

  <Section name="PaLM">
    <TextField
      label="API Key"
      bind:value={palm_key}
      password={true}
      isVertical={true}
    />
  </Section>

  <Section name="Stability">
    <TextField
      label="API Key"
      bind:value={stability_key}
      password={true}
      isVertical={true}
    />
  </Section>

  <Section name="ElevenLabs">
    <TextField
      label="API Key"
      bind:value={elevenlabs_key}
      password={true}
      isVertical={true}
    />
  </Section>

  <Section name="Cohere">
    <TextField
      label="API Key"
      bind:value={cohere_key}
      password={true}
      isVertical={true}
    />
  </Section>

  <Section name="Perplexity">
    <TextField
      label="API Key"
      bind:value={perplexity_key}
      password={true}
      isVertical={true}
    />
  </Section>

  <Section name="Speechify">
    <TextField
      label="API Key"
      bind:value={speechify_key}
      password={true}
      isVertical={true}
    />
  </Section>
</div>

<div class="row">
  <button
    class="save-auth-button"
    on:click={save_auth_config}
    disabled={save_button_text !== "Save"}
  >
    {save_button_text}
  </button>
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
    gap: 12px;
  }

  .row {
    display: flex;
    justify-content: flex-end;
    margin-top: 12px;
  }

  button {
    padding: 8px 16px;
    margin-right: 8px;
    border-radius: 4px;
    border: none;
    background-color: var(--accent-color);
    color: white;
    cursor: pointer;
  }

  button:hover {
    background-color: var(--accent-color-hover);
  }

  button:disabled {
    background-color: var(--accent-color-disabled);
    cursor: not-allowed;
  }
</style>
