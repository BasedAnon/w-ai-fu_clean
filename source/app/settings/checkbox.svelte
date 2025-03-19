<!-- Simple checkbox component -->
<script lang="ts">
    export let checked = false;
    export let disabled = false;
</script>

<label class="checkbox-wrapper" class:disabled>
    <input
        type="checkbox"
        bind:checked
        {disabled}
        on:change
    />
    <span class="checkmark"></span>
    <slot />
</label>

<style>
    .checkbox-wrapper {
        display: inline-flex;
        align-items: center;
        position: relative;
        padding-left: 26px;
        cursor: pointer;
        user-select: none;
    }

    .checkbox-wrapper.disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    input {
        position: absolute;
        opacity: 0;
        cursor: pointer;
        height: 0;
        width: 0;
    }

    .checkmark {
        position: absolute;
        left: 0;
        height: 18px;
        width: 18px;
        background-color: #333333;
        border: 1px solid #555555;
        border-radius: 3px;
    }

    .checkbox-wrapper:hover input:not(:disabled) ~ .checkmark {
        background-color: #444444;
    }

    input:checked ~ .checkmark {
        background-color: #555555;
    }

    .checkmark:after {
        content: "";
        position: absolute;
        display: none;
    }

    input:checked ~ .checkmark:after {
        display: block;
    }

    .checkbox-wrapper .checkmark:after {
        left: 6px;
        top: 2px;
        width: 4px;
        height: 9px;
        border: solid white;
        border-width: 0 2px 2px 0;
        transform: rotate(45deg);
    }
</style>
