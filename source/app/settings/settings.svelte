<!-- Main Settings Component -->
<script lang="ts">
    import { onMount } from "svelte";
    import AuthTab from "./settings_page/auth_tab.svelte";
    import { wAIfu } from "../types/Waifu";
    import { IO } from "../io/io";
    
    let activeTab = "auth"; // Default to auth tab
    
    onMount(() => {
        IO.debug("Settings page loaded");
    });
    
    const setActiveTab = (tab: string) => {
        activeTab = tab;
    };
</script>

<div class="settings-container">
    <div class="tabs">
        <div 
            class="tab" 
            class:active={activeTab === "auth"} 
            on:click={() => setActiveTab("auth")}
        >
            Accounts
        </div>
        <!-- Add more tabs as needed -->
    </div>
    
    <div class="tab-content">
        {#if activeTab === "auth"}
            <AuthTab />
        {/if}
        <!-- Add more tab content sections as needed -->
    </div>
</div>

<style>
    .settings-container {
        display: flex;
        flex-direction: column;
        height: 100%;
        color: #ffffff;
        background-color: #222222;
    }
    
    .tabs {
        display: flex;
        border-bottom: 1px solid #444444;
    }
    
    .tab {
        padding: 0.8em 1.2em;
        cursor: pointer;
        border-bottom: 2px solid transparent;
    }
    
    .tab:hover {
        background-color: #333333;
    }
    
    .tab.active {
        background-color: #333333;
        border-bottom: 2px solid #ffffff;
    }
    
    .tab-content {
        flex: 1;
        overflow: auto;
        padding: 1em;
    }
</style>
